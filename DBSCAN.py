import arcpy,os

# Overwrite existing output, by default
arcpy.env.overwriteOutput = True

arcpy.env.workspace = os.path.abspath('.')

in_features = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)
min_number = arcpy.GetParameterAsText(2)
search_distance = arcpy.GetParameterAsText(3)
cluster_sensitivity = arcpy.GetParameterAsText(4)

arcpy.stats.DensityBasedClustering(in_features,output, "DBSCAN",min_number,search_distance, cluster_sensitivity)
arcpy.AddMessage('Task finished!')