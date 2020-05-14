# load necessary packages
library(tidyverse)
library(lubridate)
library(naniar)

## prepare SNAP data for ingestion at a yearly level
# load data
snap <- read.csv('data/raw/SNAP_by_month_&_tract.csv')

# basic munging
snap$name <- as.factor(snap$name)
snap$elig_month <- as.Date(snap$elig_month)
snap <- snap %>% mutate(yr = day(elig_month), month = year(elig_month))
snap$yr <- as.factor(snap$yr)
snap$month <- as.factor(snap$month)
snap$race2 <- ifelse(snap$race2 == 'Black/African American', 'black',
              ifelse(snap$race2 == 'Asian/Pacific Islander', 'asian',
              ifelse(snap$race2 == 'Hispanic or Latino', 'other',
              ifelse(snap$race2 == 'American Indian or Alaskan Native', 'other',
              ifelse(snap$race2 == 'Other or Unknown', 'other', 'white')))))

# aggregation
monthly_snap <- snap %>% group_by(yr, month, name) %>% summarize(ppl = sum(people))
yrly_snap <- snap %>% group_by(yr, race2, name) %>% summarize(race_ppl = sum(people))
total_yrly_snap <- snap %>% group_by(yr, name) %>% summarize(total_ppl = sum(people))

# consilidate SNAP attributes to one df 
yearly_snap <- merge(yrly_snap, total_yrly_snap, by = c('yr', 'name'))

# create a proportion of people by race enrolled in SNAP
yrly_race_prop_snap <- yearly_snap %>% mutate(prop = (race_ppl / total_ppl) * 100)

# transform data to wide format
yrly_race_prop_snap <- yrly_race_prop_snap %>% select( -race_ppl) %>% rename(race = race2)
yrly_race_prop_snap_final <- yrly_race_prop_snap %>%
  spread(key = race, value = prop) %>%
  rename(total_enrolled_SNAP = total_ppl,
         asian_SNAP_enrollment_perc = asian,
         black_SNAP_enrollment_perc = black,
         other_SNAP_enrollment_perc = other,
         white_SNAP_enrollment_perc = white,
         date = yr
         )

## merge various attributes to master tract csv
df <- read.csv('data/raw/Life_expectancy_raw.CSV')
df2 <- read.csv('data/tract_mt.csv')
df3 <- read.csv('data/raw/evictions_by_tract.csv')

df_2 <- df %>% filter(df$tractID %in% df2$name) %>% # filter for only Hennepin County tracts
  rename(name = tractID, life_expectancy = mean) %>%
  select(name, life_expectancy) # select attribute of interest

df3_2 <- df3 %>% filter(year %in% c(2019, 2018, 2017, 2016)) %>% # filter for years going back to 2016
  rename(eviction_filings = Filings) %>%
  mutate(eviction_rate_perc = (Evictions / eviction_filings * 100)) %>%
  select(name, year, eviction_filings, eviction_rate_perc)

df3_2 <- df3_2 %>% rename(date = year)

# load in master tract csv
tract_update <- read.csv('data/import/tract.csv')
tract_update <- tract_update %>% select(-eviction_filings, -eviction_rate_perc)

# merge attributes and clean dataset
tract_updated <- merge(tract_update, df3_2, by = c('name', 'date'), all.x = TRUE)

tract_updated$eviction_rate_perc <- round(tract_updated$eviction_rate_perc, 0)
tract_updated$eviction_filings <- round(tract_updated$eviction_filings, 0)

tracts2 <- merge(tracts, yrly_race_prop_snap_final, by = 'name', all.x = TRUE)

tracts2 <- tracts2 %>%
  rename(estimated_perc_SNAP_households = households_on_SNAP_perc) %>%
  select(name:healthInsured_perc, mean_travel_work:eviction_rate_perc, 
         estimated_perc_SNAP_households, total_enrolled_SNAP:white_SNAP_enrollment_perc)

tracts2$asian_SNAP_enrollment_perc <- as.integer(tracts2$asian_SNAP_enrollment_perc)
tracts2$black_SNAP_enrollment_perc <- as.integer(tracts2$black_SNAP_enrollment_perc)
tracts2$other_SNAP_enrollment_perc <- as.integer(tracts2$other_SNAP_enrollment_perc)
tracts2$white_SNAP_enrollment_perc <- as.integer(tracts2$white_SNAP_enrollment_perc)

# write updated tract csv to directory
write.csv(tract_updated, 'tract_updated.csv')


## 2nd round of ingestion in the second phase of project
tract <- read.csv('data/tract_updated.csv')
county <- read.csv('data/county_updated.csv')
cities <- read.csv('data/hc_cities.csv')
city_justice <- read.csv('data/raw/city_justice_2015-2019.csv')
county_justice <- read.csv('data/raw/county_justice_2015-2019.csv')
svi <- read.csv('data/raw/SVI_avgs.csv')
hdi <- read.csv('data/raw/hdi_tract.csv')
hdi_county <- read.csv('data/raw/hdi_county.csv')

# add hdi data at a tract level
hdi <- hdi %>% filter(year > 2015 & race == 'All') # grab data for years since 2016
hdi <- hdi %>% mutate(name = paste('t', tractName, sep = '')) %>% select(name, race:Wellbeing.Index) # create tract id col
hdi <- hdi %>% filter(is.na(Education.Index) == FALSE) # removing duplicates, observed this pattern in the data
hdi <- hdi %>% select(name, year, Wellbeing.Index) %>% rename(hdi_index = Wellbeing.Index) 
hdi <- hdi %>% filter(is.na(hdi_index) == FALSE)
tract_2019 <- tract %>% filter(date == 2019)
tract_2019_update <- merge(tract_2019, hdi, by = 'name', all.x = TRUE)

# add hdi data at a county level, same process as above
hdi_county <- hdi_county %>% filter(year > 2015)
hdi_county <- hdi_county %>% filter(is.na(Education_Index) == FALSE)
hdi_county <- hdi_county %>% filter(race == 'all')
hdi_county <- hdi_county %>% select(county, year, Wellbeing_Index) %>% 
  rename(hdi_index = Wellbeing_Index)

# add svi data to master tract csv
svi <- svi %>% 
  select(TractNo, Households, SingleParent_Households, Mobile_Homes, No_HS_Diploma:Limited_English) %>%
  rename(num_households = Households, single_parent_households = SingleParent_Households,
         mobile_home_households = Mobile_Homes, no_HS_diploma_households = No_HS_Diploma, 
         no_vehicle_households = Households_No_Vehicle, limited_english_households = Limited_English, 
         name = TractNo)

svi$name <- as.character(svi$name)
tract_2019_update$name <- as.character(tract_2019_update$name)

# merge new attributes to master tract csv
tract_2019_update <- merge(tract_2019_update, svi, by = 'name', all.x = TRUE)
write.csv(tract_2019_update, 'tract_2019_update.csv')

# add county justice data
county_justice <- county_justice %>% 
  select(County, Year, num_of_cases_total, num_of_case_gender_Male, 
         num_of_case_race_Black.or.African.American:num_of_case_race_Asian,
         num_of_case_group_Adult:num_of_case_group_Juvenile, 
         num_of_case_level_Felony:num_of_case_level_Misdemeanor,
         num_of_case_level_Petty.Misdemeanor) %>%
  filter(Year %in% c(2016, 2017, 2018, 2019)) %>%
  rename(num_of_court_cases_total = num_of_cases_total,
         num_of_court_cases_male = num_of_case_gender_Male,
         num_of_court_cases_black = num_of_case_race_Black.or.African.American,
         num_of_court_cases_white = num_of_case_race_White,
         num_of_court_cases_asian = num_of_case_race_Asian,
         num_of_court_cases_adult = num_of_case_group_Adult,
         num_of_court_cases_juv = num_of_case_group_Juvenile,
         num_of_court_cases_felony = num_of_case_level_Felony,
         num_of_court_cases_gross_misd = num_of_case_level_Gross.Misdemeanor,
         num_of_court_cases_misd = num_of_case_level_Misdemeanor,
         num_of_court_cases_petty_misd = num_of_case_level_Petty.Misdemeanor, 
         name = County, date = Year)

county_justice$name <- tolower(county_justice$name)
county <- county %>% select(name:hrly_wage_w_children,hdi_index)
county_updated <- merge(county, county_justice, by = c('name', 'date'), all.x = TRUE)
write.csv(county_updated, 'county_updated.csv')

# add nearest_hospital attribute to tract csv
tracts <- read.csv('data/import/tract.csv')
hospitals <- read.csv('data/raw/hospital_tract_relationship.csv')
tracts_updated <- merge(tracts, hospitals, by = 'name', all.x = TRUE)
write.csv(tracts_updated, 'tract_updated.csv')
  
  
  
  
  
