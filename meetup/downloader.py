import multiprocessing,requests,os,time
from wsgiref import headers
from datetime import datetime,timezone
import pandas as pd

def chunk_it(seq, num):
    """divide origin list into several chunks based on the given `num`
    :param seq: the input list
    :param num: how many number of slices needed
    """
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

class Downloader(multiprocessing.Process):

    url = 'https://api.meetup.com/gql'
    query_dict = {'Outdoors & Adventure': 242, 'Tech':292, 'Family':232, 'Health & Wellness':302, 'Sports & Fitness':282,
    'Learning':562, 'Photography':262, 'Food & Drink':162, 'Writing':582, 'Language & Culture':212, 'Music':512, 'Movements':552,
    'LGBTQ':585, 'Film':583, 'Sci-Fi & Games':182, 'Beliefs':132, 'Arts':122, 'Book Clubs':222, 'Dance':542, 'Pets':252,
    'Hobbies & Crafts':532, 'Fashion & Beauty':584, 'Social':272, 'Career & Business':522}    
    headers = {'authority':'api.meetup.com',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def __init__(self,topic,query_date,query_number = 100):
        super(Downloader,self).__init__()
        self.topic = topic
        self.query_date = query_date
        self.__n = query_number

    def __query(self,query_dict = query_dict,url = url,headers = headers):
        """Query the events data from meetup server

        Args:
            query_dict ([str], optional): A dictionary contains events type and their query id used in the meetup webserver
            url ([str], optional): The meetup webserver url

        Returns:
            [json]: A json file contains events information
        """
        data = {"operationName":"categoryEvents","variables":{"topicId":query_dict[self.topic],"startDateRange":self.query_date,"lat":32.80,"lon":-96.80,"first":self.__n},"query":"query categoryEvents($lat: Float!, $lon: Float!, $topicId: Int, $startDateRange: DateTime, $endDateRange: DateTime, $first: Int, $after: String) {\n  searchEvents: upcomingEvents(search: {lat: $lat, lon: $lon, categoryId: $topicId, startDateRange: $startDateRange, endDateRange: $endDateRange}, input: {first: $first, after: $after}) {\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    count\n    recommendationSource\n    recommendationId\n    edges {\n      node {\n        group {\n          name\n          urlname\n          timezone\n          link\n          groupPhoto {\n            id\n            baseUrl\n            __typename\n          }\n          __typename\n        }\n        description\n        fee\n        feeCurrency\n        id\n        title\n        dateTime\n        eventPhoto {\n          id\n          baseUrl\n          __typename\n        }\n        venue {\n          id\n          name\n          address1\n          address2\n          address3\n          city\n          state\n          country\n          zip\n          phone\n          venueType\n          __typename\n        }\n        going {\n          totalCount\n          edges {\n            metadata {\n              memberGroupPhoto {\n                thumbUrl\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        link\n        isSaved\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        # data = {"operationName":"categoryEvents","variables":{"topicId":query_dict[self.topic],"startDateRange":self.query_date,"lat":32.80,"lon":-96.80,"first":self.__n},"query":"query categoryEvents($lat: Float!, $lon: Float!, $topicId: Int, $startDateRange: DateTime, $endDateRange: DateTime, $first: Int, $after: String) {\n  searchEvents: upcomingEvents(search: {lat: $lat, lon: $lon, categoryId: $topicId, startDateRange: $startDateRange, endDateRange: $endDateRange}, input: {first: $first, after: $after}) {\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    count\n    recommendationSource\n    recommendationId\n    edges {\n      node {\n        group {\n          name\n          urlname\n          timezone\n          link\n          groupPhoto {\n            id\n            baseUrl\n            __typename\n          }\n          __typename\n        }\n        description\n        fee\n        feeCurrency\n        id\n        title\n        dateTime\n        eventPhoto {\n          id\n          baseUrl\n          __typename\n        }\n        venue {\n          id\n          name\n          address1\n          address2\n          address3\n          city\n          state\n          country\n          zip\n          phone\n          venueType\n          __typename\n        }\n        going {\n          totalCount\n          edges {\n            metadata {\n              memberGroupPhoto {\n                thumbUrl\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        link\n        isSaved\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        events_json = requests.post(url,headers = headers,json = data).json()
        # events_json = requests.post(url,json = data).json()
        events = []
        for edge in events_json['data']['searchEvents']['edges']:
                event = {}
                event['Title'] = edge['node']['title']
                event['Date'] = edge['node']['dateTime']
                event['Group Name'] = edge['node']['group']['name']
                try:
                    event['Place'] = edge['node']['venue']['name']
                except:
                    event['Place'] = None
                try:
                    event['Zip'] = edge['node']['venue']['zip']
                    event['address1'] = edge['node']['venue']['address1']
                except:
                    event['Zip'] = None
                    event['address1'] = None
                event['Url'] = edge['node']['link']
                events.append(event)
        return events

    def __to_excel(self,events):
        et_new = pd.DataFrame(events)
        print(et_new)
        file_name = os.path.join('./events/',str(self.topic).replace(' ','-') + '.xlsx')
        try:
            if os.path.exists(file_name):
                et_old = pd.read_excel(file_name)
                et_merge = pd.concat([et_old, et_new], axis=0, sort=False).drop_duplicates(['Title','Date'],keep='last').reset_index(drop=True)
                cname = et_merge.columns
                cIndex = [s for s in cname if 'Unnamed' in s]
                for index in cIndex[1:]:
                    del et_merge[index]
                et_merge.to_excel(file_name,index=False)
            else:
                et_new.to_excel(file_name,index=False)
        except Exception as e:
            print(e)

    def run(self):
        print('Task %s start!' %self.topic)
        self.__to_excel(self.__query())
        


if __name__ == "__main__":
    
    query_dict = {'Outdoors & Adventure': 242, 'Tech':292, 'Family':232, 'Health & Wellness':302, 'Sports & Fitness':282,
    'Learning':562, 'Photography':262, 'Food & Drink':162, 'Writing':582, 'Language & Culture':212, 'Music':512, 'Movements':552,
    'LGBTQ':585, 'Film':583, 'Sci-Fi & Games':182, 'Beliefs':132, 'Arts':122, 'Book Clubs':222, 'Dance':542, 'Pets':252,
    'Hobbies & Crafts':532, 'Fashion & Beauty':584, 'Social':272, 'Career & Business':522}

    now = datetime.strftime(datetime.now(timezone.utc), "%Y-%m-%dT%H:%M:%S")

    types = list(query_dict.keys())
    types_chunk = chunk_it(types,3)
    start_time = time.time()
    for i in range(1,6):
        for threads in types_chunk:
            for thread in threads:
                p = Downloader(thread,now)
                p.start()
            p.join()
        time.sleep(300)    
    print('Task finished with %s seconds' %(round(time.time() - start_time, 2)))

