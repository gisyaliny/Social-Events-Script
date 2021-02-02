import arcpy,time

arcpy.env.overwriteOutput = True
# set workspace environment
arcpy.env.workspace = r'F:\Social-Events\Shapefile\MetropPolitan'


# set input polygon
input = r'F:\Social-Events\Shapefile\MetropPolitan\Dallas_FortWorth_Arlington.shp'

outFeatureClass = "Dallas-Fishnetby100.shp"
outFeatureClass1 = "Dallas-grids.shp"


# Set coordinate system of the output fishnet
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("US National Atlas Equal Area")

arcpy.Project_management(input,'Projected_Dallas.shp', arcpy.env.outputCoordinateSystem )
try:
    start_time = time.time()
    point_Array = []
    for row in arcpy.da.SearchCursor('Projected_Dallas.shp', ["SHAPE@",'*','OID@']):
        point_Array.append(row[0].centroid)
        extent = row[0].extent
    print(point_Array)
    cellSizeWidth = '100'
    cellSizeHeight = '100'

    # Set the origin of the fishnet
    originCoordinate = str(extent.XMin) + ' ' + str(extent.YMin)

    # Set the orientation
    yAxisCoordinate = str(extent.XMin) + ' ' + str(extent.YMin + int(cellSizeWidth))

    # Create a point label feature class 
    # labels = 'LABELS'

    # Each output cell will be a polygon
    geometryType = 'POLYGON'

    numRows =  str(int((extent.YMax-extent.YMin) / int(cellSizeHeight)) + 10 )
    numColumns = str(int((extent.XMax-extent.XMin) / int(cellSizeHeight)) +10 )

    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, geometry_type=geometryType)

    # Male a Layer from the feature class
    arcpy.MakeFeatureLayer_management(outFeatureClass, 'finshnet')
    arcpy.MakeFeatureLayer_management(input, "Mask")

    # Filter layer by given mask layer
    arcpy.SelectLayerByLocation_management('finshnet', "INTERSECT", "Mask", "", "NEW_SELECTION")

    # Write the selected features to a new featureclass
    arcpy.CopyFeatures_management('finshnet', outFeatureClass1)
    end_time = time.time()
    print('Transformation finished with %s Seconds' % (round(end_time - start_time, 2)))
except:
   print(arcpy.GetMessages())
