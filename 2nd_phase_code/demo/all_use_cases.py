# load necessary packages
from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

# establish connection with graph
graph = Graph('http://localhost:7474', password='cypha2')


## Increase post secondary education
# plot the relationships of district attributes
# query the db
df = pd.DataFrame(graph.run("""

MATCH (d:District)
WHERE d.date = 2018 
RETURN d.name, d.avg_ACT, d.num_teachers, d.pop_5_17, d.num_households_poverty

""").data())

# clean query results
df = df.dropna()
df = df[df['d.name'] != 'Minneapolis Public']
df['students_per_teacher'] = df['d.pop_5_17'] / df['d.num_teachers']

# plot pdf of act scores
act = df['d.avg_ACT']
sns.kdeplot(data=act.values, shade=True)
plt.show(block=True)
plt.interactive(False)

# plot scatter of num household in poverty vs act scores
sns.scatterplot(x=df['d.num_households_poverty'], y=df['d.avg_ACT'])
plt.show(block=True)
plt.interactive(False)

# plot of num households in poverty with trendline
sns.regplot(x=df['d.num_households_poverty'], y=df['d.avg_ACT'], ci=None)
plt.show(block=True)
plt.interactive(False)

# plot scatter of students per teacher vs act scores
sns.scatterplot(x=df['students_per_teacher'], y=df['d.avg_ACT'])
plt.show(block=True)
plt.interactive(False)

# query db for tracts with low ACT scores
df2 = pd.DataFrame(graph.run("""

MATCH (d:District)
WHERE d.name IN ['Anoka-Hennepin Public', 'Brooklyn Center', 'Osseo Public', 'Richfield Public', 'Robbinsdale Public']
RETURN d.name, d.date, d.avg_ACT

""").data())

# plot lineplot of act scores for low performing districts
sns.lineplot(x=df2['d.date'], y=df2['d.avg_ACT'], hue=df2['d.name'])
plt.show(block=True)
plt.interactive(False)

# query db for tracts that are educated by the low performing districts
df3 = pd.DataFrame(graph.run("""

MATCH (d:District)-[:EDUCATES]->(t:Tract)
WHERE d.date = 2018 AND d.name IN ['Brooklyn Center', 'Richfield Public']
RETURN t.white_perc, t.black_perc, t.asian_perc, t.total_pop, t.edu_total_pop_above_25_w_bach_degree

""").data())

# query the db for all tracts in 2018
df4 = pd.DataFrame(graph.run("""

MATCH (t:Tract)
WHERE t.date = 2018
RETURN t.white_perc, t.black_perc, t.asian_perc, t.total_pop, t.edu_total_pop_above_25_w_bach_degree

""").data())

# compare the % of pop with a bach degree for tracts educated by low performing districts and all tracts
df3['pop_w_bach_degree_%'] = df3['t.edu_total_pop_above_25_w_bach_degree'] / df3['t.total_pop']
df4['pop_w_bach_degree_%'] = df4['t.edu_total_pop_above_25_w_bach_degree'] / df4['t.total_pop']
df3 = df3.mean()
df4 = df4.mean()

# query the db for the neighborhoods that locate in the tracts that are educated by Brooklyn Center & Richfield
df5 = pd.DataFrame(graph.run("""

MATCH (d:District)-[:EDUCATES]->(t:Tract)<-[:LOCATES_IN]-(n:Neighborhood)
WHERE d.date = 2018 AND d.name IN ['Brooklyn Center', 'Richfield Public']
RETURN n.total_cases,  t.total_pop

""").data())

# query the db for all tracts and neighborhoods in 2018
df6 = pd.DataFrame(graph.run("""

MATCH (t:Tract)<-[:LOCATES_IN]-(n:Neighborhood)
WHERE t.date = 2018
RETURN n.total_cases,  t.total_pop

""").data())

# compare the cases per capita for neighborhoods educated by low performing districts and all neighborhoods
df5['cases_per_capita'] = df5['n.total_cases'] / df5['t.total_pop']
df6['cases_per_capita'] = df6['n.total_cases'] / df6['t.total_pop']

df5.mean()
df6.mean()

## Increase housing supports to reduce homelessness
# query graph database
df7 = pd.DataFrame(graph.run("""
MATCH (t:Tract) WHERE t.date = 2018 
RETURN t.inc_income_below_poverty_perc
""").data())

# plot pdf of % of pop with income below poverty
density(df7)

# query graph
df8 = pd.DataFrame(graph.run("""
MATCH (t:Tract) WHERE t.date = 2018 RETURN t.hs_subsidized_units, t.hs_occupied_units
""").data())

df9 = pd.DataFrame(graph.run("""
MATCH (t:Tract) 
WHERE t.date = 2018 AND t.name IN ["t3003800", "t3005901", "t3005902", "t3103900", "t3104000", "t3104800", "t3104900", "t3105700", "t3106000", "t3106200", "t3126000"] 
RETURN t.hs_subsidized_units, t.hs_occupied_units
""").data())

# transformations
df8 = df8.replace(-1, 0)
df8 = df8.dropna()
df9 = df9.replace(-1, 0)
df9 = df9.dropna()
df8['subsidized_unit_%'] = df8['t.hs_subsidized_units'] / df8['t.hs_occupied_units']
df9['subsidized_unit_%'] = df9['t.hs_subsidized_units'] / df9['t.hs_occupied_units']

# calculate all tract avg % of housing units subsidized
round(df8['subsidized_unit_%'].mean() * 100, 1)

# calculate impoverished pocket of tracts avg % of housing units subsidized
round(df9['subsidized_unit_%'].mean() * 100, 1)

