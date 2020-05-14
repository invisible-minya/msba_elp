# load necessary packages
from py2neo import Graph
import pandas as pd

# establish connection with db
graph = Graph('http://localhost:7474', password = 'cypher1')

# 2a) Do minority dominant neighborhoods have a disproportionate school enrollment rate? 
# 2b)What is the avg act score of the districts that educate these tracts?

# queries
df1 = pd.DataFrame(graph.run("MATCH (d:District)-[:EDUCATES]->(t:Tract) WHERE t.black_perc > 30 \
        RETURN t.name AS tract, t.black_perc AS prop_black, t.k_12_enrolled_perc AS perc_enrolled_k_12, d.avg_ACT AS avg_ACT \
                             ORDER BY t.black_perc DESC LIMIT 25").data())

df2 = pd.DataFrame(graph.run("MATCH (d:District)-[:EDUCATES]->(t:Tract) WHERE t.white_perc > 90 \
        RETURN t.name AS tract, t.white_perc AS prop_white, t.k_12_enrolled_perc AS perc_enrolled_k_12, d.avg_ACT AS avg_ACT\
                             ORDER BY t.white_perc DESC LIMIT 25").data())

# transformations
black_enrollment = df1['perc_enrolled_k_12'].mean()
white_enrollment = df2['perc_enrolled_k_12'].mean()
black_act = df1['avg_ACT'].mean()
white_act = df2['avg_ACT'].mean()
data = {'race':['white', 'black'], 'k_12_enrollment':[white_enrollment, black_enrollment], 'avg_ACT': [white_act, black_act]}
plot_df = pd.DataFrame(data)

# write csv for dashboard
plot_df.to_csv('/Users/bradyengelke/MSBA/spring/ELP/minority_tracts.csv')

# 3) For tracts with SNAP enrollment rate above 25 vs SNAP enrollment rate below 5, 
# what is the percentage of the population that attends undergrad?

# queries
df3 = pd.DataFrame(graph.run("MATCH (t:Tract) WHERE t.households_on_SNAP_perc > 25 \
    RETURN t.name AS tract, t.households_on_SNAP_perc AS households_on_snap_perc, t.college_undergrad_perc AS undergrad_perc \
                             ORDER BY t.households_on_SNAP_perc DESC").data())

df4 = pd.DataFrame(graph.run("MATCH (t:Tract) WHERE t.households_on_SNAP_perc < 3 \
    RETURN t.name AS tract, t.households_on_SNAP_perc AS households_on_snap_perc, t.college_undergrad_perc AS undergrad_perc \
                             ORDER BY t.households_on_SNAP_perc DESC").data())

# transformations
high_snap = df3['undergrad_perc'].mean()
low_snap = df4['undergrad_perc'].mean()
data1 = {'snap_enrollment':['high', 'low'], 'undergrad_perc': [high_snap, low_snap]}
plot_df2 = pd.DataFrame(data1)

# write csv for dashboard
plot_df2.to_csv('/Users/bradyengelke/MSBA/spring/ELP/snap_tracts.csv')

# 4a) What is the HDI of tracts across HC? 
# 4b) What is the racial distribution of tracts with lowest HDI vs highest HDI?

# queries
df5 = pd.DataFrame(graph.run("MATCH (c:County)-[:SERVES]->(t:Tract) WHERE c.name = 'hennepin' \
        RETURN c.life_expectancy AS life_expectancy, t.college_undergrad_perc AS undergrad_perc, t.k_12_enrolled_perc AS k_12_enrollment, \
        t.income_median AS income_median, t.white_perc AS white_perc, t.black_perc AS black_perc, t.asian_perc AS asian_perc, \
        t.other_ethnicity_perc AS other_perc, t.name AS tract").data())

# transformations
df5['hdi'] = (df5['life_expectancy'] + (df5['undergrad_perc'] * 3) + df5['k_12_enrollment'] + (df5['income_median'] / 1000)) / 4
low_hdi = df5[df5['hdi'] < df5['hdi'].mean() - df5['hdi'].std()]
high_hdi  = df5[df5['hdi'] > df5['hdi'].mean() + df5['hdi'].std()]
hdi_all = df5[['tract', 'hdi']]
low_hdi_avg = low_hdi['hdi'].mean()
high_hdi_avg = high_hdi['hdi'].mean()
all_hdi_avg = hdi_all['hdi'].mean()
low_hdi_race = pd.DataFrame(low_hdi[['white_perc', 'black_perc', 'asian_perc', 'other_perc']].mean())
high_hdi_race = pd.DataFrame(high_hdi[['white_perc', 'black_perc', 'asian_perc', 'other_perc']].mean())
data2 = {'hdi_level':['low', 'middle' ,'high'], 'hdi': [low_hdi_avg, all_hdi_avg, high_hdi_avg]}
plot_df3 = pd.DataFrame(data2)

# write csv for dashboard
plot_df3.to_csv('/Users/bradyengelke/MSBA/spring/ELP/hdi_avg.csv')

# transformations
data3 = {'race':['white', 'black', 'asian', 'other'], 'perc_of_pop': [low_hdi_race.values[0][0], low_hdi_race.values[1][0], low_hdi_race.values[2][0], low_hdi_race.values[3][0]]}
plot_df4 = pd.DataFrame(data3)

# write csv for dashboard
plot_df4.to_csv('/Users/bradyengelke/MSBA/spring/ELP/low_hdi_race.csv')

# transformations
data3 = {'race':['white', 'black', 'asian', 'other'], 'perc_of_pop': [high_hdi_race.values[0][0], high_hdi_race.values[1][0], high_hdi_race.values[2][0], high_hdi_race.values[3][0]]}
plot_df4 = pd.DataFrame(data3)

# write csv for dashboard
plot_df4.to_csv('/Users/bradyengelke/MSBA/spring/ELP/high_hdi_race.csv')

