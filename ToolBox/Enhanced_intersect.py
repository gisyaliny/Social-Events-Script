import arcpy,os,glob

# Overwrite existing output, by default
arcpy.env.overwriteOutput = True

def enhanced_clip(outdir,mask,indir = '',infc =''):
    """[Clip all shapefiles within the input directory with given mask layer and export them into given output directory]

    Args:
        indir ([str]): [input directory contains shapefiles need to be cliped]
        outdir ([type]): [output directory]
        mask ([type]): [absolute path of the mask layer]
    """
    arcpy.env.workspace = outdir
    if infc:
        feature_lst = [infc]
    else:
        feature_lst = glob.glob(os.path.join(indir,'*.shp'))
    arcpy.MakeFeatureLayer_management(mask, "Mask")
    try:
        for index,feature in enumerate(feature_lst):
            outname = os.path.splitext(os.path.basename(feature))[0]
            # Male a Layer from the feature class
            arcpy.MakeFeatureLayer_management(feature, str(index))
            # Filter layer by given mask layer
            arcpy.SelectLayerByLocation_management(str(index), "INTERSECT", "Mask", "", "NEW_SELECTION")
            # Write the selected features to a new featureclass
            arcpy.CopyFeatures_management(str(index), outname)
            print(outname)

            ## Add the output Layer into Arcgis pro
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            arcpy.MakeFeatureLayer_management(outname, outname)
            addLayer = arcpy.mapping.Layer(outname)
            arcpy.mapping.AddLayer(df,addLayer)
    except:
        print(arcpy.GetMessages())

indir = arcpy.GetParameterAsText(0)
infc = arcpy.GetParameterAsText(1)
outdir = arcpy.GetParameterAsText(2)
mask = arcpy.GetParameterAsText(3)

if infc:
    enhanced_clip(outdir,mask,infc=infc)
else:
    enhanced_clip(outdir,mask,indir=indir)



# def test():
#     indir = os.path.abspath(r'F:\Social-Events\Shapefile\Social-Events')
#     mask = r'F:\Social-Events\Shapefile\MetropPolitan\Dallas_FortWorth_Arlington.shp'
#     outdir = r'F:\Social-Events\Shapefile\Events-After-Clip'
#     enhanced_clip(indir,outdir,mask)

# if __name__ == "__main__":
#     test()




