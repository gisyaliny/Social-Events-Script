import os,glob,time
import pandas as pd
import geopandas as gpd


def drop_na(df):
    drop_lst = [colnam for colnam in df.columns if ('Unnamed' in colnam)]
    df.drop(drop_lst, axis=1, inplace=True)
    df = df.dropna()
    return df

def list_file(path,extension):
    """Return list of files with specific extension within the given path """
    return glob.glob(os.path.join(path,'*.'+extension))


def to_shp(file_lst,outpath,Date_format,type = 'csv',key_x ='X',key_y = 'Y',\
            prj = {'init': 'epsg:4326'},):
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
            if Date_format:
                gdf['Date'] =  gdf['Date'].map(lambda x: x.strftime(Date_format))
            fn = os.path.join(outpath, os.path.splitext(os.path.basename(file))[0] + '.shp')
            try:
                gdf.to_file(fn)
                print('Transfer ' + fn + ' successful!')
            except Exception as e:
                # print(fn + ' already exist!')
                print(str(e))
        else:
            continue
    end_time = time.time()
    print('Transformation finished with %s Seconds' % (round(end_time - start_time, 2)))