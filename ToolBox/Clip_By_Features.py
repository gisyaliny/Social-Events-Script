import arcpy,os
# Overwrite existing output, by default
arcpy.env.overwriteOutput = True

# arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = os.path.abspath('../Data/POI/Maptitude_POI/Shp')

# mask = arcpy.GetParameterAsText(1)
mask = r'F:\Social-Events\Shapefile\Zillow\dallas_city_limit_nolakes.shp'

# output_path = arcpy.GetParameterAsText(2)
output_path = '../Shapefile/POI'

feature_lst =arcpy.ListFeatureClasses('.')
print(os.listdir(arcpy.env.workspace))
print(feature_lst)
for feature in feature_lst:
    output = os.path.join(output_path , os.path.basename(feature))
    print(output)
    arcpy.Intersect_analysis(feature,output,'','','point')