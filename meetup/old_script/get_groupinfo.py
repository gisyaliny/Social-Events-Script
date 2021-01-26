'''
This is a program to get all the information about groups
'''
import sys
sys.path.append(r'F:\geostats')

from geostats import Scraping
from urllib.request import Request
import urllib.request

def get_groupsInfo(url):
    opener = Scraping.setProxy()
    urllib.request.install_opener(opener)
    content = Scraping.parseHtml(url)
    Name = Scraping.list2string(content.xpath('//*[@id="mupMain"]/div/div/section/div/div/div/div/h1/a[@class="groupHomeHeader-groupNameLink"]//text()'),'')
    detail1 = content.xpath('//div[@class="group-description--wrapper"]/div/div/p//text()')
    try:
        detail = Scraping.list2string(detail1, '\n')
    except:
        detail = ''
    try:
        Organizers = Scraping.list2string(
            content.xpath('//*[@id="organizer"]/div/div/div/div/div/div/div/div[@class="flex-item"]//text()'), '')
    except:
        Organizers = ''
    try:
        address = dataClean.list2string(content.xpath(
            '//*[@id="mupMain"]/div/div/section/div/div/div/div/div/div/div/ul[@class="organizer-city"]//text()'), '')
    except:
        address = ''
    Photo_Cover = content.xpath('//*[@id="mupMain"]/div/div/section/div/div/div/div/div/@style')
    try:
        Photo_Cover_url = str(Scraping.url_FromString(Photo_Cover[0])[0]).replace(")", "")
    except:
        Photo_Cover_url = ''
    try:
        Members = Scraping.list2string(content.xpath(
            '//*[@id="mupMain"]/div/div/section/div/div/div/div/div/div/div/ul[@class="inlineblockList inlineblockList--separated"]//text()'),
                              ' ').replace('?', "")
    except:
        Members = ''
    try:
        related_topics = Scraping.list2string(content.xpath(
            '//*[@id="mupMain"]/div/div/div/section/div/div[@class="topicsList flush--left margin--top"]//text()'),
                                     " @ ")
    except:
        related_topics = ''
    record = {"Name": Name, "What we're about": detail, "Organizers": Organizers, "Location": address,
              "Cover_Photo": Photo_Cover_url, "Members": Members, "Related topics": related_topics}
    return record


def main():
    url1 = "https://www.meetup.com/Hiking-with-Geeks-Dallas/"
    record = get_groupsInfo(url1)
    print(record)


if __name__ == '__main__':
    main()