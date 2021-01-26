##DBScan
library(rgdal);library(magrittr);library(dbscan);library(ggplot2);library(sf)
library(factoextra);library(ggpubr);library(concaveman);library(readxl)

setwd("F:\\Social-Events\\Shapefile\\Social-Events")

files <- list.files(pattern = ".shp$")

df <- read_excel("F:\\Social-Events\\Script\\Classified_events.xlsx")
df_sf <- as_Spatial(st_as_sf(df, coords = c("Long", "Lat"),crs = 4326))

dfproj <- spTransform(df_sf, CRS("+init=epsg:32138"))
dataframe = as.data.frame(dfproj@data)
location <- dfproj@coords
bf_dbscan <- dbscan(location,700,100)
bf_dbscan

nrow(location)
p2 <- fviz_cluster(bf_dbscan, location, geom = "point", pointsize = 1,shape = 1)+
  scale_color_brewer('Cluster', palette='Set2')+
  scale_fill_brewer('Cluster', palette='Set2')+
  theme(legend.position = "none")+
  ggtitle("")
plot(p2,ncol = 1, nrow = 1,labels = c("13/14", "15"))

dfproj@data$DbScan <- bf_dbscan$cluster
group <- unique(dataframe$DbScan)
group


tot_hull_after <- list()
for(g in 1:length(group))
{
  concave <- concaveman(subset(location, dfproj@data$DbScan == group[g]),concavity = 1.4)
  num_cluster <- round(nrow(subset(location, dfproj@data$DbScan == group[g]))/nrow(dfproj)*100,3)
  concave$cluster <- gsub(" ","",paste(num_cluster,"%"))
  tot_hull_after[[g]] <- concave
}
tot_hull_after
??concaveman








