library(tidyverse)
library(dplyr)
# This reads in the original SVI data from the CDC
SVI_MN <- read.csv("Minnesota.csv")
SVI_MN

#Select Hennepin County Specifically
SVI_Hennepin <- SVI_MN[SVI_MN$COUNTY == "Hennepin",]
SVI_Hennepin
# This narrows down the last few digits of the county tract ids that match with the rest of the project
SVI_Hennepin$FIPS <- SVI_Hennepin$FIPS-27050000000
SVI_Hennepin$FIPS <- sub("^", "t", SVI_Hennepin$FIPS)

# Add a column for the year this dataset came from
SVI_Hennepin$Year <- 2018
SVI_Hennepin

#Pull out the Chosen Attributes. There are many others that may be relevant
#But we chose to bring these in for our project. You can probably store the rest in the database as necessary.
#There are also some others here, but if we found them in ACS, we chose not to include them from here.
SVI_RawNumbers <- SVI_Hennepin %>% select("FIPS", "Year", "E_HH", "E_DISABL", "E_UNINSUR", "E_SNGPNT", "E_MOBILE", 
                                          "E_NOHSDP", "E_NOVEH", "E_LIMENG")
# Rename to fit the database format
SVI_RawNumbers <- SVI_RawNumbers%>%rename("TractNo"="FIPS","Year"= "Year","hs_num_households"= "E_HH",
                                          "hl_disabled"= "E_DISABL","hl_uninsured" =  "E_UNINSUR","hs_single_parent_households" ="E_SNGPNT",
                                          "hs_mobile_home_households"= "E_MOBILE", "edu_no_HS_diploma_households" = "E_NOHSDP",
                                          "t_no_vehicle_households" ="E_NOVEH", "edu_limited_english_households" ="E_LIMENG")


#Repeat for the margins of errors
SVI_MarginsOfError <- SVI_Hennepin %>% select("FIPS", "Year", "E_HH", "E_DISABL", "E_UNINSUR", "E_SNGPNT", "E_MOBILE", 
                                          "E_NOHSDP", "E_NOVEH", "E_LIMENG")
# Rename to fit the database format
SVI_MarginsOfError <- SVI_MarginsOfError%>%rename("TractNo"="FIPS","Year"= "Year","hs_num_households_MoE"= "M_HH",
                                          "hl_disabled_MoE"= "M_DISABL","hl_uninsured_MoE" =  "M_UNINSUR","hs_single_parent_households_MoE" ="M_SNGPNT",
                                          "hs_mobile_home_households_MoE"= "M_MOBILE", "edu_no_HS_diploma_households_MoE" = "M_NOHSDP",
                                          "t_no_vehicle_households_MoE" ="M_NOVEH", "edu_limited_english_households_MoE" ="M_LIMENG")
