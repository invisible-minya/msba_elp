## 3rd round of data ingestion in 2nd phase of project
# load necessary packages
import pandas as pd

# load datasets
tract = pd.read_csv('data/tract.csv')
district = pd.read_csv('data/district.csv')
health = pd.read_csv('data/HC_health_stats_by_tract.csv')
edu = pd.read_csv('data/edu_statistics_by_district.csv')
housing = pd.read_csv('data/Subsidized_housing_by_tract.csv')

# create a column name mapping
cols_old = ['hl_BINGE_CrudePrev', 'hl_BPHIGH_CrudePrev', 'hl_CANCER_CrudePrev',
            'hl_CASTHMA_CrudePrev', 'hl_CHD_CrudePrev', 'hl_CHECKUP_CrudePrev',
            'hl_CSMOKING_CrudePrev', 'hl_DENTAL_CrudePrev', 'hl_KIDNEY_CrudePrev',
            'hl_MHLTH_CrudePrev', 'hl_OBESITY_CrudePrev', 'hl_SLEEP_CrudePrev',
            'hl_STROKE_CrudePrev']

cols_new = ['hl_binge_drinking_prev', 'hl_high_blood_pressure_prev', 'hl_cancer_prev',
            'hl_asthma_prev', 'hl_heart_disease_prev', 'hl_doctor_visits_prev', 'hl_smoking_prev',
            'hl_dentist_visits_prev',  'hl_kidney_disease_prev',  'hl_poor_mental_health_prev',
            'hl_obesity_prev', 'hl_poor_sleep_prev', 'hl_stroke_prev']

# create new df to append columns to in following loop
health_new = health[['TractFIPS', 'date']]

# loop through original health csv and grab only columns of interest and append to new health csv
for col in health.columns:
    i = 0
    for old_col in cols_old:
        if old_col == col:
            health_new[cols_new[i]] = health[col]
        i += 1

health_new = health_new.rename(columns={'TractFIPS': 'name'})

# merge attributes to master tract csv
tract_updated = tract.merge(health_new, on=['name', 'date'], how='left')
tract_updated = tract_updated.merge(housing, on=['name', 'date'], how='left')
tract_updated.to_csv('data/tract_updated.csv', index=False)

# merge attributes to master district csv
district_updated = district.merge(edu, on=['districtId', 'date'], how='left')
district_updated.to_csv('data/district_updated.csv', index=False)

## add new ACS data to master tract csv
new_acs = pd.read_csv('data/new_tract_acs.csv')
old_tract = pd.read_csv('data/tract.csv')
new_tract = old_tract.merge(new_acs, on=['name', 'date'], how='left')
new_tract.to_csv('data/tract_updated.csv', index=False)

# add city entity to logical model
city = pd.read_csv('data/city.csv')
city_adj = pd.read_csv('data/city_adj.csv')

# grab only city to city relationships that are valid
indices = []
i = 0
for id1, id2 in zip(city_adj.cityId1.values, city_adj.cityId2.values):
    if (id1 in city.cityId.values) and (id2 in city.cityId.values):
        indices.append(i)
    else:
        indices = indices
    i += 1

new_city_adj = city_adj.iloc[indices]
new_city_adj.to_csv('data/city_adj_updated.csv', index=False)

# grab only cities to tract relationships that are valid
city = pd.read_csv('data/city.csv')
tracts = pd.read_csv('data/tract.csv')
city_tract = pd.read_csv('data/hc_city_tract.csv')
indices = []
i = 0
for tid, cid in zip(city_tract.name.values, city.cityId.values):
    if (cid in city.cityId.values) and (tid in tracts.name.values):
        indices.append(i)
    else:
        indices = indices
    i += 1

new_city_tract = city_tract.iloc[indices]
new_city_tract.to_csv('data/city_tract_updated.csv', index=False)

# grab only tract to tract relationships that are valid
tract_adj = pd.read_csv('data/hc_tract_neighbour_to.csv')
indices = []
i = 0
for tid1, tid2 in zip(tract_adj.name1.values, tract_adj.name2.values):
    if (tid1 in tracts.name.values) and (tid2 in tracts.name.values):
        indices.append(i)
    else:
        indices = indices
    i += 1

new_tract_adj = tract_adj.iloc[indices]
new_tract_adj.to_csv('data/tract_adj_updated.csv', index=False)

# grab only neighborhood to tract relationships that are valid
neigh_tract = pd.read_csv('data/neighborhood_tract.csv')
indices = []
i = 0
for tid in neigh_tract.name.values:
    if tid1 in tracts.name.values:
        indices.append(i)
    else:
        indices = indices
    i += 1

new_n_tract = neigh_tract.iloc[indices]
new_n_tract.to_csv('data/tract_adj_updated.csv', index=False)

## add crime attributes to neighborhood nodes
# load and clean datasets
neigh = pd.read_csv('data/neighborhood.csv')
p2016 = pd.read_csv('data/Police_Incidents_2016.csv')
p2017 = pd.read_csv('data/Police_Incidents_2017.csv')
p2018 = pd.read_csv('data/Police_Incidents_2018.csv')
p = pd.concat([p2016, p2017, p2018])
p['month'] = p.date.map(lambda x: x[5:7])
del p['date']

# map types of crime to a higher level categorization
mapping = {'Other Theft': 'theft',
           'Robbery Of Person': 'theft',
           'Burglary Of Dwelling': 'theft',
           'Robbery Per Agg': 'theft',
           'Burglary Of Business': 'theft',
           'Theft From Motr Vehc': 'theft',
           'Motor Vehicle Theft': 'theft',
           'Arson': 'arson',
           'Robbery Of Business': 'theft',
           'Shoplifting': 'theft',
           'Theft By Swindle': 'theft',
           'Theft From Person': 'theft',
           'Theft-motr Veh Parts': 'theft',
           'Aslt-sgnfcnt Bdly Hm': 'assault',
           '2nd Deg Domes Aslt': 'assault',
           'Theft From Building': 'theft',
           '3rd Deg Domes Aslt': 'assault',
           'Bike Theft': 'theft',
           'Asslt W/dngrs Weapon': 'assault',
           'Domestic Assault/Strangulation': 'assault',
           'Aslt-police/emerg P': 'assault',
           'On-line Theft': 'theft',
           'Disarm a Police Officer': 'assault',
           'Scrapping-Recycling Theft': 'theft',
           'Crim Sex Cond-rape': 'rape',
           'Murder (general)': 'murder',
           'Other Vehicle Theft': 'theft',
           'Aslt-great Bodily Hm': 'assault',
           'Theft/coinop Device': 'theft',
           '1st Deg Domes Asslt': 'assault',
           'Gas Station Driv-off': 'theft',
           'Theft By Computer': 'theft',
           'Pocket-picking': 'theft'}

p['description'] = p['description'].map(mapping)
del p['offense']

# aggregation
p_yrly = p.groupby(by=['name', 'year', 'description']).count().reset_index()
total_yrly = p.groupby(by=['name', 'year']).count().reset_index()
total_yrly = total_yrly.rename(columns={'month': 'total_cases'})
p_yrly = p_yrly.rename(columns={'month': 'count'})

# convert data to a wide format
p_yrly = p_yrly.pivot_table(index=['name', 'year'], columns='description', values='count')
total_yrly = total_yrly.set_index(['name', 'year'])
p_yrly['total_cases'] = total_yrly['total_cases']
p_yrly = p_yrly.reset_index().fillna(0)

# create new proportional cols and delete old cols 
p_yrly['arson_perc'] = round((p_yrly['arson'] / p_yrly['total_cases']) * 100, 0)
del p_yrly['arson']
p_yrly['theft_perc'] = round((p_yrly['theft'] / p_yrly['total_cases']) * 100, 0)
del p_yrly['theft']
p_yrly['assault_perc'] = round((p_yrly['assault'] / p_yrly['total_cases']) * 100, 0)
del p_yrly['assault']
p_yrly['murder_perc'] = round((p_yrly['murder'] / p_yrly['total_cases']) * 100, 0)
del p_yrly['murder']
p_yrly['rape_perc'] = round((p_yrly['rape'] / p_yrly['total_cases']) * 100, 0)
del p_yrly['rape']

# merge attributes to master neighborhood csv
p_yrly = p_yrly.rename(columns={'year': 'date'})
neigh_new = neigh.merge(p_yrly, on=['name', 'date'], how='left')
neigh_new.to_csv('data/neighborhood_updated.csv', index=False)

# can complete same process at a monthly level, if necessary
p_mnthly = p.groupby(by=['name', 'year', 'month', 'description']).count().reset_index()
total_mnthly = p.groupby(by=['name', 'year', 'month']).count().reset_index()

# add median rent to tract.csv
tract = pd.read_csv('data/tract.csv')
rent = pd.read_csv('data/tract_rent.csv')
tract = tract.merge(rent, on=['name', 'date'], how='left')
tract.to_csv('data/tract_updated.csv')

# final SNAP data update
tract = pd.read_csv('data/tract_final.csv')
acs = pd.read_csv('data/acs_snap.csv')
tract_updated = tract.merge(acs, on=['name', 'date'], how='left')
tract_updated.to_csv('data/tract_updated_final.csv', index=False)

# move court case data to city granularity instead of county granularity
# load and clean csvs
city = pd.read_csv('data/city_old2.csv')
court_cases = pd.read_csv('data/city_crime_atts.csv')
del court_cases['City']

# merge new court_cases attributes
city_new = city.merge(court_cases, on=['cityId', 'date'], how='left')
city_new = city_new.fillna(0)
city_new.to_csv('data/city_uptodate.csv', index=False)
