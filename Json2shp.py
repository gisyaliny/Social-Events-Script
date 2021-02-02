import sys
sys.path.append('.')
import functions,os,time
import geopandas as gpd

start_time = time.time()

data_dir = r'F:\Social-Events\Data\POI\Maptitude_POI'

json_lst = functions.list_file(data_dir,extension='json')

outdir = r'F:\Social-Events\Data\POI\Maptitude_POI\Shp'

for file in json_lst:
    df = gpd.read_file(file)
    outname = os.path.splitext(os.path.basename(file))[0]
    print(outname)
    df.to_file(os.path.join(outdir,outname.strip().replace(' ','-') + '.shp'))

end_time = time.time()
print('Transformation finished with %s Seconds' % (round(end_time - start_time, 2)))
