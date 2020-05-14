library(neo4r)
library(tidyverse)
library(ggfortify)
library(stats)
library(magrittr)
library(naniar)
library(lubridate)

con <- neo4j_api$new(
  url = 'http://localhost:7474',
  user = "neo4j", 
  password = 'cypha2'
)

data <- 'MATCH (t:Tract) WHERE t.date = 2019 
RETURN t.name, t.total_pop, t.median_age, t.white_perc, t.black_perc, t.asian_perc, 
       t.hdi_index, t.emp_unemployed_perc, t.edu_k_12_enrolled_perc, 
       t.edu_college_undergrad_perc, t.edu_stem_degree_perc, t.edu_no_HS_diploma_households, 
       t.edu_limited_english_households, t.hl_health_insured_perc, t.hl_life_expectancy, 
       t.hs_eviction_rate_perc, t.inc_income_median, t.inc_total_enrolled_SNAP' %>%
  call_neo4j(con)

df <- as.data.frame(data)
df <- df %>% rename(
  name = value,
  pop = value.1,
  age = value.2,
  white_perc = value.3,
  black_perc = value.4,
  asian_perc = value.5,
  hdi = value.6,
  unemployed_perc = value.7,
  k_12_enrolled_perc = value.8,
  undergrad_perc = value.9,
  stem_degree_perc = value.10,
  no_HS_diploma_households = value.11, 
  limited_english_households = value.12,
  insured_perc = value.13,
  life_exp = value.14,
  income = value.16, 
  SNAP_enroll = value.17
) %>%
  select(-value.15)
 
miss_var_summary(df)
df <- na.omit(df)
atts <- df %>%
  select(age, unemployed_perc:SNAP_enroll)
 
tract_atts_pca <- prcomp(atts, center = TRUE, scale. = TRUE)
print(tract_atts_pca)
summary(tract_atts_pca)
plot(tract_atts_pca, type = "l")

autoplot(tract_atts_pca)
autoplot(tract_atts_pca, data = atts,
         loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)

tract_pcs <- data.frame(tract_atts_pca$x[,1:5])

SSE_curve <- c()
for (n in 1:10) {
  kcluster <- kmeans(tract_pcs, n)
  sse <- sum(kcluster$withinss)
  SSE_curve[n] <- sse
}
plot(1:10, SSE_curve, type="b", xlab="Number of Clusters", ylab="SSE")

k = 4
tract_pca_clusters <- kmeans(tract_pcs, k, nstart = 20)
pca_clustered_tracts <- df %>% mutate(cluster = tract_pca_clusters$cluster)
miss_var_summary(pca_clustered_tracts)
pca_clustered_tracts_avgs <- pca_clustered_tracts %>%
  group_by(cluster) %>%
  summarize_all('mean')
  
  
  