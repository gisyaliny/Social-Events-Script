########################################
## DBScan algorithm
setwd("E:\\NIST\\DBScan\\sf_meter")
dbf_f <- read.dbf(gsub(" ","",paste(dow[w],wkhr[h],"_", number,".dbf")))
dbf_f_after <- read.dbf(gsub(" ","",paste(dow[w],wkhr[h],"_", number_after,".dbf")))

df <- dbf_f[,14:15]
df_after <- dbf_f_after[,14:15]

bf_dbscan <- dbscan(df,2600,3)
bf_dbscan$cluster
after_dbscan <- dbscan(df_after,2700,3)
after_dbscan

p2 <- fviz_cluster(bf_dbscan, df, geom = "point", pointsize = 1,shape = 1)+
  scale_color_brewer('Cluster', palette='Set2')+
  scale_fill_brewer('Cluster', palette='Set2')+
  theme(legend.position = "none")+
  ggtitle("")


p3 <- fviz_cluster(after_dbscan, df_after, geom = "point",shape = 1)+
  scale_color_brewer('Cluster', palette='Set2')+
  scale_fill_brewer('Cluster', palette='Set2')+
  theme(legend.position = "none")+
  ggtitle("")

ggarrange(p2,p3,ncol = 2, nrow = 1,labels = c("13/14", "15"))

road <- as_Spatial(read_sf(dsn = "E:\\NIST\\DBScan\\sf_meter\\road_type.shp"))


