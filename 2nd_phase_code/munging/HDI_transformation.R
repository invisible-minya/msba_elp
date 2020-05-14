
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


# Check lengths of GEOID field values
unique(lapply(as.character(hdi$GEOID), nchar))

# Extract last 7 digits of GEOID as tract name and add 't' as prefix
hdi$tractName <- substr(as.character(hdi$GEOID), 5, 11)


# Check available years
unique(hdi$year)
# [1] 2013 2018

# Check available races
unique(hdi$race)
# [1] All                    Asian                  Black/African American Hispanic/Latinx        Native American       
# [6] White (Non-Hispanic)

# Check number of tracts in data
length(unique(hdi$tractName))
# [1] 299


# remove columns that are not required
hdi2 <- hdi %>% select('tractName', 'year', 'race', 'index', 'estimate')


# Separate the 4 indices
#hdi2 <- spread(hdi2, index, estimate)
hdi2 <- hdi2 %>% 
  group_by_at(vars(-estimate)) %>%  # group by everything other than the value column. 
  mutate(row_id=1:n()) %>% ungroup() %>%  # build group index
  spread(key=index, value=estimate) %>%    # spread
  select(-row_id) 

# Check if data is at tractName, year, race level
hdi2 %>% mutate(x=paste0('tractName', 'year', 'race')) %>% unique() %>% count()
# 3638


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

# Export HDI data as csv
write.csv(hdi2, 'hdi_tract.csv', row.names=FALSE)
