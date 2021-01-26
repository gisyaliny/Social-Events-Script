import os,sys
sys.path.append(os.path.abspath('..'))
from functions import merge_df
import datetime,time
import pandas as pd
from glob import glob

def getevevnts(path,category,group):
    try:
        df1 = pd.read_excel(os.path.join(path,"events.xlsx"))
        df1['Category'] = category
        df1['Group'] = group
        return df1
    except:
        print(str(os.path.join(path,"events.xlsx")) + ' do not exist')


def getDate(dateString):
    date_time = []
    start_time =[]
    end_time = []
    for row in dateString:
        day = str(row).split(",")[0]
        month = str(row).split(",")[1]
        year = str(str(row).split(",")[2])[:5]
        try:
            start_time.append(str(row).split(",")[2].replace(year,'').split('to')[0])
        except:
            start_time.append('None')
        try:
            end_time.append(str(row).split(",")[2].replace(year,'').split('to')[-1])
        except:
            end_time.append('None')
        timeString = day + ',' + month + ',' + year
        date_obj = datetime.datetime.strptime(timeString, '%A, %B %d, %Y')
        date_time.append(date_obj.strftime("%m-%d-%Y"))

    return date_time,start_time,end_time

def events2df(categories_path,df_path):
    taks_start_time = time.time()
    categories = glob(categories_path)
    df = pd.read_excel(df_path)
    origin_nrow = len(df.index)
    for category_path in categories:
        category = str(category_path).split("\\")[-1]
        groups = os.listdir(category_path)
        groups.remove(category + ".xlsx")
        for group in groups:
            group_path = os.path.join(category_path,group)
            df1 = getevevnts(group_path,category,group)
            df = pd.concat([df, df1], axis=0, sort=False)

    df = merge_df.clean_index(df)
    df = df.dropna(subset=['Location','Hold Date'])
    df = df.drop_duplicates(subset=['Name','Description','Hold Date']).reset_index(drop=True)
    df['Lat'] = df['Location'].map(lambda x: str(x).split(";")[0])
    df['Long'] = df['Location'].map(lambda x: str(x).split(";")[1])
    date_time,start_time,end_time = getDate(df['Hold Date'])
    df['Date'] = date_time
    df['Start_Time'] = start_time
    df['End_Time'] = end_time
    print('Task finished with %f seconds, updates %d events' %(round(time.time()-taks_start_time,2), len(df.index)-origin_nrow))
    df.to_excel(df_path)

def main():
    categories_path = os.path.abspath("../Data/*/")
    df_path = os.path.abspath('../../../events.xlsx')
    events2df(categories_path,df_path)

if __name__ == '__main__':
    main()