from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

graph = Graph('http://localhost:7474', password='cypha2')

hc_df = pd.DataFrame(graph.run("""
                                
MATCH (c:County) WHERE c.name = 'hennepin'
RETURN c.date, c.total_pop, c.rural_pop_perc, c.black_perc, c.white_perc, c.hdi_index, 
       c.hl_yrs_life_lost_rate, c.hl_pop_smokers_perc, c.hl_pop_obese_perc,
       c.hl_pop_drink_in_excess_perc, c.hl_teen_birth_rate, c.hl_uninsured_perc,
       c.hl_num_physicians, c.hl_num_therapists, c.hl_overdose_rate,
       c.j_court_cases_total, c.j_court_cases_male, c.j_court_cases_black,
       c.j_court_cases_white, c.j_court_cases_asian, c.j_court_cases_adult, 
       c.j_court_cases_juv, c.j_court_cases_felony, c.inc_pop_poor_perc, 
       c.inc_percentile_80_income, c.inc_percentile_20_income, c.inc_free_lunch_perc, 
       c.emp_unemployed_perc
                            
""").data())

hc_tracts = pd.DataFrame(graph.run("""

MATCH (t:Tract) WHERE t.date = 2019
RETURN t.name, t.total_pop, t.median_age, t.white_perc, t.black_perc, t.asian_perc, 
       t.hdi_index, t.emp_unemployed_perc, t.edu_k_12_enrolled_perc, 
       t.edu_college_undergrad_perc, t.edu_stem_degree_perc, t.edu_no_HS_diploma_households, 
       t.edu_limited_english_households, t.hl_health_insured_perc, t.hl_life_expectancy, 
       t.hs_eviction_filings, t.hs_eviction_rate_perc, t.inc_income_median, 
       t.inc_total_enrolled_SNAP, t.inc_households_on_SNAP_perc_est

""").data())

hc_tracts_monthly_df = pd.DataFrame(graph.run("""

MATCH (tm:Tract_m)-[:BELONGS_TO]->(t:Tract)<-[:SERVES]-(c:County) WHERE c.name = 'hennepin'
RETURN tm.name AS tractId, tm.year AS year, tm.month AS month, t.total_pop AS tract_pop,
       tm.total_enrolled_SNAP AS total_enrolled_SNAP

""").data())


