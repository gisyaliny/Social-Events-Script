import os,glob,time
import geopandas as gpd
import pandas as pd

def list_dir(path):
    """Return list of the sub directory within the given path"""
    return [f.path for f in os.scandir(path) if f.is_dir()]

def list_file(path,extension):
    """Return list of files with specific extension within the given path """
    return glob.glob(os.path.join(path,'*.'+extension))

def to_shp(file_lst,outpath,type = 'csv',key_x ='X',key_y = 'Y',prj = {'init': 'epsg:4326'}):
    """Transfer files to shapefile under the given out path"""
    start_time = time.time()
    for file in file_lst:
        if type == 'csv':
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        if (df.shape[0] > 2):
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[key_x], df[key_y]))
            gdf.crs = prj
            gdf = gdf.to_crs(epsg=2163)
            fn = os.path.join(outpath, os.path.splitext(file)[0] + '.shp')
            try:
                gdf.to_file(fn)
                print('Transfer ' + fn + ' successful!')
            except:
                print(fn + ' already exist!')
        else:
            continue
    end_time = time.time()
    print('Transformation finished with %s Seconds' % (round(end_time - start_time, 2)))

if __name__ == "__main__":
    path = '.'
    excel_lst= list_file(path,extension='xlsx')
    print(excel_lst)
