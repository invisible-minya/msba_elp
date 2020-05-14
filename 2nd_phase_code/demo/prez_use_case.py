from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

def density(df):
    sns.kdeplot(data=df['t.inc_income_below_poverty_perc'].values, shade=True)
    plt.show(block=True)
    plt.interactive(False)

# establish graph connection
graph = Graph('http://localhost:7474', password='cypha2')

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

# data transformations
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
