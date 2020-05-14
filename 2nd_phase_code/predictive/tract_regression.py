# import packages
from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import statsmodels.api as sm
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

# establish connection & query
graph = Graph('http://localhost:7474', password='cypha2')
tracts = pd.DataFrame(graph.run("""

MATCH (t:Tract) WHERE t.date = 2019
RETURN t.name as tractId, t.total_pop AS pop, t.median_age AS median_age, t.white_perc, t.black_perc, t.asian_perc,
       t.hdi_index AS hdi, t.emp_unemployed_perc, t.edu_k_12_enrolled_perc, t.edu_college_undergrad_perc,
       t.edu_total_pop_above_25_w_bach_degree AS adults_w_bach_degree, t.edu_no_HS_diploma_households, 
       t.hl_health_insured_perc, t.hl_life_expectancy AS life_expectancy, 
       t.hs_occupied_housing_units, t.hs_rented_housing_units,
       t.hs_num_households, t.hs_single_parent_households, t.hs_mobile_home_households, 
       t.inc_income_median AS median_income, t.t_mean_travel_work, t.t_no_vehicle_households, 
       t.inc_total_enrolled_SNAP
       
""").data())

# clean query results & engineer features
tracts['t.edu_no_HS_diploma_households'] = tracts['t.edu_no_HS_diploma_households'].fillna(tracts['t.edu_no_HS_diploma_households'].median())
tracts['t.hs_num_households'] = tracts['t.hs_num_households'].fillna(tracts['t.hs_num_households'].median())
tracts['t.hs_single_parent_households'] = tracts['t.hs_single_parent_households'].fillna(tracts['t.hs_single_parent_households'].median())
tracts['t.hs_mobile_home_households'] = tracts['t.hs_mobile_home_households'].fillna(tracts['t.hs_mobile_home_households'].median())
tracts['t.t_no_vehicle_households'] = tracts['t.t_no_vehicle_households'].fillna(tracts['t.t_no_vehicle_households'].median())
tracts['t.inc_total_enrolled_SNAP'] = tracts['t.inc_total_enrolled_SNAP'].fillna(0)

tracts['adults_w_bach_degree_perc'] = tracts['adults_w_bach_degree'] / tracts['pop']
del tracts['adults_w_bach_degree']
tracts['pop_enrolled_SNAP_perc'] = tracts['t.inc_total_enrolled_SNAP'] / tracts['pop']
del tracts['t.inc_total_enrolled_SNAP']
tracts['no_vehicle_households_perc'] = tracts['t.t_no_vehicle_households'] / tracts['t.hs_num_households']
del tracts['t.t_no_vehicle_households']
tracts['single_parent_households_perc'] = tracts['t.hs_single_parent_households'] / tracts['t.hs_num_households']
del tracts['t.hs_single_parent_households']
tracts['mobile_home_households_perc'] = tracts['t.hs_mobile_home_households'] / tracts['t.hs_num_households']
del tracts['t.hs_mobile_home_households']
del tracts['t.hs_num_households']
tracts['rented_housing_units_perc'] = tracts['t.hs_rented_housing_units'] / tracts['t.hs_occupied_housing_units']
del tracts['t.hs_occupied_housing_units']
del tracts['t.hs_rented_housing_units']

# add ACT attribute to tracts frame
act = pd.DataFrame(graph.run("""

MATCH (d:District)-[:EDUCATES]->(t:Tract) WHERE t.date = 2019 
RETURN t.name as tractId, d.avg_ACT AS act_score

""").data())

act = act.groupby(by='tractId').mean()
act = act.reset_index()
tracts = tracts.merge(act, on='tractId')

# add nearest hospital attribute to tracts frame
nearest_hospitals = pd.read_csv('data/tract_nearest_hospitals.csv')
tracts = tracts.merge(nearest_hospitals, on='tractId')

# finish cleaning frame
del tracts['tractId']
del tracts['pop']
del tracts['hdi']

tracts['sorter'] = np.random.randn(299)
tracts = tracts.sort_values(by='sorter').reset_index()
del tracts['index']
del tracts['sorter']

## predict life expectancy at a tract level ##
tracts_hl = tracts.dropna()
life_exp_y = tracts_hl['life_expectancy']
life_exp_x = tracts_hl
del life_exp_x['life_expectancy']

life_exp_y_train = life_exp_y.loc[:235]
life_exp_y_test = life_exp_y.loc[236:]
life_exp_x_train = life_exp_x.loc[:235, :]
life_exp_x_test = life_exp_x.loc[236:, :]

# OLS
test_model = sm.OLS(life_exp_y_train, life_exp_x_train).fit()
life_exp_preds = test_model.predict(exog=life_exp_x_test)
mean_squared_error(life_exp_y_test.values, life_exp_preds.values)

life_exp_model = sm.OLS(life_exp_y, life_exp_x)
life_exp_results = life_exp_model.fit()
print(life_exp_results.summary())

# Decision Tree
life_exp_test_dt = DecisionTreeRegressor().fit(life_exp_x_train, life_exp_y_train)
life_exp_dt_preds = life_exp_test_dt.predict(life_exp_x_test)
mean_squared_error(life_exp_y_test.values, life_exp_dt_preds)

life_exp_dt = DecisionTreeRegressor().fit(life_exp_x, life_exp_y)
data = {'feature': life_exp_x.columns, 'importance': life_exp_dt.feature_importances_}
life_exp_fi = pd.DataFrame(data).sort_values(by='importance', ascending=False)

## predict education attainment at a tract level ##
edu_y = tracts['adults_w_bach_degree_perc']
edu_x = tracts
edu_x['life_expectancy'] = edu_x['life_expectancy'].fillna(edu_x['life_expectancy'].median())
del edu_x['adults_w_bach_degree_perc']

edu_y_train = edu_y.loc[:240]
edu_y_test = edu_y.loc[241:]
edu_x_train = edu_x.loc[:240, :]
edu_x_test = edu_x.loc[241:, :]

# OLS
test_edu_model = sm.OLS(edu_y_train, edu_x_train).fit()
edu_preds = test_edu_model.predict(exog=edu_x_test)
mean_squared_error(edu_y_test.values, edu_preds.values)

edu_model = sm.OLS(edu_y, edu_x)
edu_results = edu_model.fit()
print(edu_results.summary())

# Decision Tree
edu_test_dt = DecisionTreeRegressor().fit(edu_x_train, edu_y_train)
edu_dt_preds = edu_test_dt.predict(edu_x_test)
mean_squared_error(edu_y_test.values, edu_dt_preds)

edu_dt = DecisionTreeRegressor().fit(edu_x, edu_y)
data = {'feature': edu_x.columns, 'importance': edu_dt.feature_importances_}
edu_fi = pd.DataFrame(data).sort_values(by='importance', ascending=False)

## predict income at a tract level ##
inc_y = tracts['median_income']
inc_x = tracts
inc_x['life_expectancy'] = inc_x['life_expectancy'].fillna(inc_x['life_expectancy'].median())
del inc_x['median_income']

inc_y_train = inc_y.loc[:240]
inc_y_test = inc_y.loc[241:]
inc_x_train = inc_x.loc[:240, :]
inc_x_test = inc_x.loc[241:, :]

# OLS
test_inc_model = sm.OLS(inc_y_train, inc_x_train).fit()
inc_preds = test_inc_model.predict(exog=inc_x_test)
mean_squared_error(inc_y_test.values, inc_preds.values)

inc_model = sm.OLS(inc_y, inc_x)
inc_results = inc_model.fit()
print(inc_results.summary())

# Decision Tree
inc_test_dt = DecisionTreeRegressor().fit(inc_x_train, inc_y_train)
inc_dt_preds = life_exp_dt.predict(inc_x_test)
mean_squared_error(inc_y_test.values, inc_dt_preds)

inc_dt = DecisionTreeRegressor().fit(inc_x, inc_y)
data = {'feature': inc_x.columns, 'importance': inc_dt.feature_importances_}
inc_fi = pd.DataFrame(data).sort_values(by='importance', ascending=False)


