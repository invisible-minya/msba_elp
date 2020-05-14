# import packages
from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

# establish connection & query
graph = Graph('http://localhost:7474', password='cypha2')
counties = pd.DataFrame(graph.run("""

MATCH (c:County)
RETURN c.name AS county, c.date AS year, c.total_pop AS pop, c.rural_pop_perc, 
       c.black_perc, c.white_perc, c.asian_perc, c.hispanics_perc, 
       c.hl_yrs_life_lost_rate AS life_lost_rate, c.hl_pop_smokers_perc, c.hl_pop_obese_perc,
       c.hl_pop_drink_in_excess_perc, c.hl_teen_birth_rate, c.hl_uninsured_perc,
       c.hl_num_physicians, c.hl_num_therapists, c.hl_overdose_rate, c.inc_pop_poor_perc, 
       c.inc_free_lunch_perc, c.emp_unemployed_perc

""").data())

# clean query results
def cleaner(x):
    if x > 100:
        x = x / 10
    elif x > 1000:
        x = x / 100
    else:
        x = x
    return x

counties['c.emp_unemployed_perc'] = counties['c.emp_unemployed_perc'].map(cleaner)
counties['c.hl_num_therapists'] = counties['c.hl_num_therapists'].fillna(0)
counties['c.inc_free_lunch_perc'] = counties['c.inc_free_lunch_perc'].fillna(int(round(counties['c.inc_free_lunch_perc'].mean())))

del counties['year']
del counties['county']

# split data into train & test
counties['sorter'] = np.random.rand(100)
counties = counties.sort_values(by='sorter').reset_index()
del counties['index']
del counties['sorter']
y = counties['life_lost_rate']
del counties['life_lost_rate']
del counties['pop']
x = counties
y_train = y[:80]
y_test = y[80:]
x_train = x.loc[:79, :]
x_test = x.loc[80:, :]

x.corr()  # concerned that inc & emp attributes explained the same variation in target, weak correlations

# exploratory plots
def density_plot(x):
    p = sns.kdeplot(x)
    p = plt.show(block=True)
    p = plt.interactive(False)
    return p

density_plot(y)
y.std()

density_plot(x['c.hl_pop_smokers_perc'])
density_plot(x['c.hl_pop_drink_in_excess_perc'])
density_plot(x['c.hl_pop_obese_perc'])
density_plot(x['c.hl_num_physicians']) # values over 1000?
density_plot(x['c.hl_num_therapists'])
density_plot(x['c.hl_overdose_rate'])

# predict life_lost_rate @ a county level
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

# test model mse
model2 = sm.OLS(y_train, x_train).fit()
preds = model2.predict(exog=x_test)
mean_squared_error(y_test.values, preds.values)
