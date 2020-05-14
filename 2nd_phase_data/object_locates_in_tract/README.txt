# this is a demonstration for locating object to tract
# load hospital data
LOAD CSV WITH HEADERS FROM 'file:///HC_hospitals.csv' AS row
WITH row.OBJECTID AS HospitalId, row.NAME AS Hospital_Name, row.ADDRESS AS Hopital_Address, row.CITY AS City, row.ZIP AS ZIP,row.LIC_TYPE AS Hospital_Type,row.HLTH_SYS AS HLTH_SYS, row.HOSP_BEDS AS HOSP_BEDS, row.BASS_BEDS AS BASS_BEDS, row.HOSP18_BED AS HOSP18_BED, row.POINT_X AS Longitude, row.POINT_Y AS Latitude
MERGE (h:Hospital {HospitalId:HospitalId})
SET h.HospitalId = HospitalId, h.Hospital_Name = Hospital_Name,h.Hopital_Address = Hopital_Address,h.City= City, h.ZIP = ZIP,h.Hospital_Type = Hospital_Type, h.HLTH_SYS = HLTH_SYS, h.HOSP_BEDS = HOSP_BEDS, h.BASS_BEDS = BASS_BEDS, h.HOSP18_BED = HOSP18_BED, h.Longitude = Longitude, h.Latitude = Latitude
RETURN count(h)

# establish hostipal and tract relationship
MATCH(h:Hospital)
CALL spatial.withinDistance('TractGeom',{latitude: toFloat(h.Latitude), longitude:toFloat(h.Longitude)},0.01)
YIELD node AS t
MERGE (h)-[rel:locate_in]->(t)
return count(rel)
