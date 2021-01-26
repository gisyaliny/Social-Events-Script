library(cluster);library(raster)
library(fpc);
library(leaflet);library(sp)
library(concaveman)
library(htmlwidgets)
library(htmltools)

boundary <- as_Spatial(read_sf(dsn = "F:\\Social-Events\\Shapefile\\Zillow\\dallas_city_limit_nolakes.shp"))
new_boundary <- spTransform(boundary, CRS("+proj=longlat +datum=NAD83 +no_defs +ellps=GRS80 +towgs84=0,0,0"))
# g <- 1
# nrow(subset(shp_15, cluster == group[g]))
# group <- unique(shp_15$cluster)
# group <- group[which(group>0)]
# group
# tot_hull_after <- list()
# for(g in 1:length(group))
# {
#   
#   concave <- concaveman(subset(shp_15, cluster == group[g]),concavity = 1.4)
#   num_cluster <- round(nrow(subset(shp_15, cluster == group[g]))/nrow(shp_15)*100,3)
#   concave$cluster <- gsub(" ","",paste(num_cluster,"%"))
#   tot_hull_after[[g]] <- concave
# }

tag.map.title <- tags$style(HTML("
  .leaflet-control.map-title { 
    transform: translate(-50%,20%);
    position: fixed !important;
    left: 50%;
    text-align: center;
    padding-left: 10px; 
    padding-right: 10px; 
    background: rgba(255,180,255,0.75);
    font-weight: bold;
    font-size: 20px;
  }
"))

outliers_after <- as.numeric(nrow(subset(location, dfproj@data$DbScan == 0)))
title <- tags$div(
  tag.map.title, HTML(c("2015 Year",
                        "total points:",nrow(location),
                        "distance:2700",
                        "minPts:3",
                        "outliers:",outliers_after))
)  

a <- leaflet() %>%
  addCircles(data = location,
             lat = location[,2],
             lng = location[,1],
             color = "red",
             radius = 0.3,fillColor = "transparent") %>%
  addPolygons(data = tot_hull_after[[1]],
              color = "red",
              fill = "red",
              fillColor = "transparent",weight = 3,
              label=as.character(tot_hull_after[[1]]$cluster),
              labelOptions = labelOptions(noHide = T,direction = "top",
                                          offset = c(0, -15))) %>%
  addPolygons(data = tot_hull_after[[2]],
              color = "red",
              fill = "red",
              fillColor = "transparent",weight = 3,
              label=as.character(tot_hull_after[[2]]$cluster),
              labelOptions = labelOptions(noHide = T,direction = "top",
                                          offset = c(0, -15)))%>%
    addPolygons(data = tot_hull_after[[3]],
                color = "red",
                fill = "red",
                fillColor = "transparent",weight = 3,
                label=as.character(tot_hull_after[[3]]$cluster),
                labelOptions = labelOptions(noHide = T,direction = "top",
                                            offset = c(0, -15)))%>%
    addPolygons(data = tot_hull_after[[4]],
                color = "red",
                fill = "red",
                fillColor = "transparent",weight = 3,
                label=as.character(tot_hull_after[[4]]$cluster),
                labelOptions = labelOptions(noHide = T,direction = "top",
                                            offset = c(0, -15)))%>%
    addPolygons(data = tot_hull_after[[5]],
                color = "red",
                fill = "red",
                fillColor = "transparent",weight = 3,
                label=as.character(tot_hull_after[[5]]$cluster),
                labelOptions = labelOptions(noHide = T,direction = "top",
                                            offset = c(0, -15)))%>%
    # addPolygons(data = tot_hull[[6]],
    #             color = "red",
    #             fill = "red",
    #             fillColor = "transparent",weight = 3,
    #             label=as.character(tot_hull_after[[6]]$cluster),
    #             labelOptions = labelOptions(noHide = T,direction = "top",
    #                                         offset = c(0, -15)))%>%
    addPolygons(data = new_boundary,
                color = "black",
                fill = "black",
                fillColor = "transparent",
                weight = 2)%>%
  addTiles() %>%
  addControl(title, position = "topleft", className="map-title")%>%
  addProviderTiles(providers$CartoDB.Positron)

  
a
