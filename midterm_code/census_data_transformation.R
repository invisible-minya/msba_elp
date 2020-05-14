library(dplyr)
library(tidyverse)
# 1. load files
income <- read.csv('your directory/ACS_17_5YR_S1901_with_ann.csv', header = T, skip = 1)
hc_tract <- read.csv('your directory/tract_district_concise.csv', header = T) # contains only Hennepin Countycensus tract 


# 2. select and rename columns
colnames(income)
colnames(income)[1] = = 'census_general_id'
colnames(income)[2] = = 'Track_id'

income_hc <- income %>%
  filter(Track_id %in% hc_tract$TRACT)
unique(income_hc$Track_id)

colnames(income_hc)

income_hc_selected <-  income_hc %>%
  select(2,3,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,
         60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108)
view(head(income_hc_selected))

colnames(income_hc_selected)
colnames(income_hc_selected)[1] = "Track_id"                                                                        
colnames(income_hc_selected)[2] =  "Geography"                                                                       
colnames(income_hc_selected)[3] = "Households_Estimate_Less_than_10_000"                                         
colnames(income_hc_selected)[4] = "Families_Estimate_Less_than_10_000"                                           
colnames(income_hc_selected)[5] = "Married_couple_families_Estimate_Less_than_10_000"                            
colnames(income_hc_selected)[6] = "Nonfamily_households_Estimate_Less_than_10_000"                               
colnames(income_hc_selected)[7] = "Households_Estimate_10_000_to_14_999"                                        
colnames(income_hc_selected)[8] = "Families_Estimate_10_000_to_14_999"                                          
colnames(income_hc_selected)[9] = "Married_couple_families_Estimate_10_000_to_14_999"                           
colnames(income_hc_selected)[10] = "Nonfamily_households_Estimate_10_000_to_14_999"                              
colnames(income_hc_selected)[11] = "Households_Estimate_15_000_to_24_999"                                        
colnames(income_hc_selected)[12] = "Families_Estimate_15_000_to_24_999"                                          
colnames(income_hc_selected)[13] = "Married_couple_families_Estimate_15_000_to_24_999"                           
colnames(income_hc_selected)[14] = "Nonfamily_households_Estimate_15_000_to_24_999"                              
colnames(income_hc_selected)[15] = "Households_Estimate_25_000_to_34_999"                                        
colnames(income_hc_selected)[16] = "Families_Estimate_25_000_to_34_999"                                          
colnames(income_hc_selected)[17] = "Married_couple_families_Estimate_25_000_to_34_999"                           
colnames(income_hc_selected)[18] = "Nonfamily_households_Estimate_25_000_to_34_999"                              
colnames(income_hc_selected)[19] = "Households_Estimate_35_000_to_49_999"                                        
colnames(income_hc_selected)[20] = "Families_Estimate_35_000_to_49_999"                                          
colnames(income_hc_selected)[21] = "Married_couple_families_Estimate_35_000_to_49_999"                           
colnames(income_hc_selected)[22] = "Nonfamily_households_Estimate_35_000_to_49_999"                              
colnames(income_hc_selected)[23] = "Households_Estimate_50_000_to_74_999"                                        
colnames(income_hc_selected)[24] = "Families_Estimate_50_000_to_74_999"                                          
colnames(income_hc_selected)[25] = "Married_couple_families_Estimate_50_000_to_74_999"                           
colnames(income_hc_selected)[26] = "Nonfamily_households_Estimate_50_000_to_74_999"                              
colnames(income_hc_selected)[27] = "Households_Estimate_75_000_to_99_999"                                        
colnames(income_hc_selected)[28] = "Families_Estimate_75_000_to_99_999"                                          
colnames(income_hc_selected)[29] = "Married_couple_families_Estimate_75_000_to_99_999"                           
colnames(income_hc_selected)[30] = "Nonfamily_households_Estimate_75_000_to_99_999"                              
colnames(income_hc_selected)[31] = "Households_Estimate_100_000_to_149_999"                                      
colnames(income_hc_selected)[32] = "Families_Estimate_100_000_to_149_999"                                        
colnames(income_hc_selected)[33] = "Married_couple_families_Estimate_100_000_to_149_999"                         
colnames(income_hc_selected)[34] = "Nonfamily_households_Estimate_100_000_to_149_999"                            
colnames(income_hc_selected)[35] = "Households_Estimate_150_000_to_199_999"                                      
colnames(income_hc_selected)[36] = "Families_Estimate_150_000_to_199_999"                                        
colnames(income_hc_selected)[37] = "Married_couple_families_Estimate_150_000_to_199_999"                         
colnames(income_hc_selected)[38] = "Nonfamily_households_Estimate_150_000_to_199_999"                            
colnames(income_hc_selected)[39] = "Households_Estimate_200_000_or_more"                                          
colnames(income_hc_selected)[40] = "Families_Estimate_200_000_or_more"                                            
colnames(income_hc_selected)[41] = "Married_couple_families_Estimate_200_000_or_more"                             
colnames(income_hc_selected)[42] = "Nonfamily_households_Estimate_200_000_or_more"                                
colnames(income_hc_selected)[43] = "Households_Estimate_Median_income_dollars_"                                   
colnames(income_hc_selected)[44] = "Families_Estimate_Median_income_dollars_"                                     
colnames(income_hc_selected)[45] = "Married_couple_families_Estimate_Median_income_dollars_"                      
colnames(income_hc_selected)[46] = "Nonfamily_households_Estimate_Median_income_dollars_"                         
colnames(income_hc_selected)[47] = "Households_Estimate_Mean_income_dollars_"                                     
colnames(income_hc_selected)[48] = "Families_Estimate_Mean_income_dollars_"                                       
colnames(income_hc_selected)[49] = "Married_couple_families_Estimate_Mean_income_dollars"                        
colnames(income_hc_selected)[50] = "Nonfamily_households_Estimate_Mean_income_dollars"                           
colnames(income_hc_selected)[51] = "Households_Estimate_PERCENT_ALLOCATED_Household_income_in_the_past_12_months"

# 3. export files to local drive
write.csv(income_hc_selected,'your directory/uncome_hc.csv')


