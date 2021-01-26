'''
This is a program to get latest 4 events from every groups
'''
import sys
sys.path.append(r'F:\geostats')

from geostats import Scraping
import pandas as pd
from urllib.request import Request
import urllib.request

def get_eventsInfo(url1):
    opener = Scraping.setProxy()
    urllib.request.install_opener(opener)
    content = Scraping.parseHtml(url1)
    try:
        events_number = Scraping.number_FromString(Scraping.list2string(content.xpath('//*[@id="mupMain"]/div/div/div/div/div/section/div/div/h3/span/text()'),''))[0]
        if events_number > 4:
            events_number = 4
    except:
        events_number = 0
    events = content.xpath('//a[@class="eventCard--link"]//text()')[:events_number]
    events_url = content.xpath('//a[@class="eventCard--link"]/@href')[:events_number]
    events_df = []
    for i,url in enumerate(events_url):
        url = 'https://www.meetup.com' + url
        content1 = Scraping.parseHtml(url)
        datetime = Scraping.list2string(content1.xpath('//div[1]/div[1]/div/section/div[2]/div/section/div[1]/div/div[2]/div/time//text()'),"")
        keywords = Scraping.list2string(content1.xpath('/html/head/meta[@name="keywords"]/@content'),'')
        description = Scraping.list2string(content1.xpath('/html/head/meta[@name="description"]/@content'),'')

        detail = Scraping.list2string(content1.xpath(
            '//div[1]/div[2]/div/div/section[1]/div/div[@class = "event-description runningText"]//text()'),"\n")
        Hoster = Scraping.list2string(content1.xpath('//div/div/div/div/div/div/div/a/span/span/span[@class="text--bold event-hosts-info-no-link"]//text()'),"")
        googlemap_url = Scraping.list2string(content1.xpath('//*/div[1]/div[1]/div/section/div[2]/div/div/a/@href'),"")
        address = Scraping.list2string(content1.xpath('/html/head/meta[@property="geo.placename"]/@content'),'')
        photoCover = Scraping.list2string(content1.xpath('/html/head/meta[@property="og:image"]/@content'),'')
        location = Scraping.list2string(content1.xpath('/html/head/meta[@property="geo.position"]/@content'),'')
        poi = Scraping.list2string(content1.xpath('//*[@class="flex flex--row"]//address/p[1]//text()'), '')
        sub_adress = Scraping.list2string(content1.xpath('//*[@class="flex flex--row"]//address/p[2]//text()'), '')
        record = {'Name':str(events[i]),'POI':poi,'URL': url,'Host By': Hoster, 'Location': location,'Address': address,
                  'Place':sub_adress,'Description':description,'Key Words':keywords,'Hold Date': datetime,"Cover_Photo": photoCover,
                  'Google Map': googlemap_url,'Detail': detail}
        events_df.append(record)
    events_df = pd.DataFrame(events_df)
    return events_df

def main():
    url1 = "https://www.meetup.com/North-Texas-Outdoors/"
    df = get_eventsInfo(url1)
    print(df)
    df.to_excel('Example-Table/events.xlsx')

if __name__ == '__main__':
    main()


