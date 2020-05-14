
# load libraries
library(tidyr)
library(dplyr)

# load hdi file created from HDI calculation script
hdi <- read.csv(here::here("data", "hdi.csv"))

# # Load census tract names to map tract IDs using GEOID
# cen_tract <- read.csv(here::here("data", "census_tract_names.csv"))


# # Extract tract ID from Name in hdi data
# hdi$tractNum <- substr(hdi$NAME, 1, regexpr(",", hdi$NAME)-1)
# hdi$tractNum <- substr(hdi$tractNum , 14, length(hdi$tractNum)-13)


# Check available years
unique(hdi$year)
# [1] 2012 2013 2014 2015 2016 2017 2018

# Check available races
unique(hdi$race)
# [1] All                    Asian                  Black/African American      Hispanic/Latinx        Native American       
# [6] White (Non-Hispanic)

# Check available counties
unique(hdi$county)
# Hennepin

# keep columns that are required
hdi2 <- hdi %>% select('county', 'year', 'race', 'index', 'estimate')
                        # hdi_detail has MOE (Richard's orig code)

# convert count names to lowercase
hdi2$county <- tolower(hdi2$county)

# Separate the 4 indices
#hdi2 <- spread(hdi2, index, estimate)
hdi2 <- hdi2 %>% 
  group_by_at(vars(-estimate)) %>%  # group by everything other than the value column. 
  mutate(row_id=1:n()) %>% ungroup() %>%  # build group index
  spread(key=index, value=estimate) %>%    # spread
  select(-row_id) 

# Check if data is at year, race level
hdi2 %>% mutate(x=paste0(year, race)) %>% unique() %>% count()
# 42


# Change race values to match other data sources
hdi2$race <- ifelse(hdi2$race == 'Black/African American', 'black',
                    ifelse(hdi2$race == 'Asian', 'asian',
                           ifelse(hdi2$race == 'Hispanic/Latinx', 'other',
                                  ifelse(hdi2$race == 'Native American', 'other',
                                         ifelse(hdi2$race == 'Other or Unknown', 'other', 
                                                ifelse(hdi2$race == 'White (Non-Hispanic)', 'white', 'all'))))))

# Check created races
unique(hdi2$race)
#"all"   "asian" "black" "other" "white"


# Rename index columns
colnames(hdi2) <- c("county","year","race","Education_Index","Health_Index","Income_Index","Wellbeing_Index")


# Check for missing HDI values
# NAs in entire column
sum(is.na(hdi2$Wellbeing_Index))
# 38 (90.5%)

# NAs by race
hdi2 %>% group_by(race) %>% summarise(sum(is.na(Wellbeing_Index)))
# 1 all                             374
# 2 asian                           598
# 3 black                           598
# 4 other                          1196


# Export HDI data as csv
write.csv(hdi2, 'hdi_county.csv', row.names=FALSE)
