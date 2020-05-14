from py2neo import Graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

graph = Graph('http://localhost:7474', password='cypha2')

tracts = pd.DataFrame(graph.run("""

MATCH (t:Tract) WHERE t.date = 2019 
RETURN t.name, t.total_pop, t.median_age, t.white_perc, t.black_perc, t.asian_perc, 
       t.hdi_index, t.emp_unemployed_perc, t.edu_k_12_enrolled_perc, 
       t.edu_college_undergrad_perc, t.edu_stem_degree_perc, t.edu_no_HS_diploma_households, 
       t.edu_limited_english_households, t.hl_health_insured_perc, t.hl_life_expectancy, 
       t.hs_eviction_rate_perc, t.inc_income_median, t.inc_total_enrolled_SNAP
       
""").data())

cluster_df = tracts[['t.total_pop', 't.median_age', 't.emp_unemployed_perc',
                     't.edu_k_12_enrolled_perc', 't.edu_college_undergrad_perc',
                     't.hl_life_expectancy',
                     't.inc_income_median', 't.inc_total_enrolled_SNAP']]

cluster_df = cluster_df.rename(columns={
    't.total_pop': 'pop',
    't.median_age': 'age',
    't.emp_unemployed_perc': 'unemployed_perc',
    't.edu_k_12_enrolled_perc': 'k_12_perc',
    't.edu_college_undergrad_perc': 'undergrad_perc',
    't.hl_life_expectancy': 'life_exp',
    't.inc_income_median': 'income',
    't.inc_total_enrolled_SNAP': 'SNAP_enrollment'
})

cluster_df = cluster_df.dropna()
tracts_scaled = StandardScaler().fit_transform(cluster_df)

x = list(range(1, 9))
y = []
for i in list(range(1, 9)):
    km = KMeans(n_clusters=i).fit(tracts_scaled)
    y.append(km.inertia_)

sns.lineplot(x=x, y=y)
plt.show(block=True)
plt.interactive(False)

km_final = KMeans(n_clusters=5).fit(tracts_scaled)
cluster_df['cluster'] = km_final.labels_
clustered_tract_avgs = cluster_df.groupby('cluster').mean()
clustered_tract_avgs = clustered_tract_avgs.round(2)


