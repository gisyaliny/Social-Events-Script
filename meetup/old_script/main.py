import sys
sys.path.append(r'F:\geostats')

from geostats import Scraping
from get_groupinfo import *
from get_eventsInfo import *
from urllib.error import HTTPError
import time,random,os

def generate_groupdf(groups):
    groups_df = []
    for j,group in enumerate(groups):
        try:
            record = get_groupsInfo(group_url[j])
            print('Get into %s' %group_url[j])
            record.update({'group': group})
            groups_df.append(record)
            new_path = os.path.join(path, str(group).strip())
            os.makedirs(new_path)
            events_df = get_eventsInfo(group_url[j])
            events_path = os.path.join(new_path,'events.xlsx')
            try:
                df1 = pd.read_excel(events_path)
                df1 = Scraping.clean_index(df1)
                events_df_new = Scraping.dfmerge(df1, events_df, ['Name','Hold Date'], 'rbind')
            except:
                events_df_new = events_df
            events_df_new.to_excel(events_path)
            print("Updates%s successful" %group)
        except(Exception):
            continue
    groups_df = pd.DataFrame(groups_df)
    return groups_df

opener = Scraping.setProxy()
urllib.request.install_opener(opener)

url = "https://www.meetup.com/"
content = Scraping.parseHtml(url)
Categories = content.xpath('//*[@id="mupMain"]/div[3]/div/section[3]/div[2]/ul/li/div/div/a/h4/text()')
Sub_Url_10miles = list(content.xpath('//*[@id="mupMain"]/div[3]/div/section[3]/div[2]/ul/li/div/div/a/@href'))
Sub_Url = [url_10miles + '?allMeetups=false&radius=50&userFreeform=Dallas%2C+TX&mcId=z75201&mcName=Dallas%2C+TX&sort=default' for url_10miles in Sub_Url_10miles]
random_lst = list(range(0,len(Sub_Url)))
random.shuffle(random_lst)

for random_index in random_lst:
    url1 = Sub_Url[random_index]
    type = str(Categories[random_index])
    path = os.path.join("./Data/", type)
    content1 = Scraping.parseHtml(url1)
    group1 = content1.xpath('//*[@id="simple-view"]/div[1]/ul/li/div/a[2]/div[2]/h3/text()')
    groups = Scraping.clean_punctuationList(group1)
    group_url = content1.xpath('//*[@id="simple-view"]/div/ul/li/div/a[@itemprop="url"]/@href')
    groups_df = generate_groupdf(groups)
    group_excel = os.path.join(path, type + ".xlsx")
    try:
        df1 = pd.read_excel(group_excel)
        df1 = Scraping.clean_index(df1)
        groups_df_new = Scraping.dfmerge(df1,groups_df,'Name','rbind')
    except(HTTPError):
        continue
    except:
        groups_df_new = groups_df
    groups_df_new.to_excel(group_excel)
    time.sleep(0.1)