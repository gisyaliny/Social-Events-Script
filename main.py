import os,sys
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('./data_mining/'))
from data_mining import main as data_mining
from data_mining.tabulation import data_processing as data_processing
from data_mining.tabulation import get_events as get_events


# if we need update our data
updates = True

# Get the events data from www.meetup.com
if updates == True:
    data_mining.main()

# Tabulate the events info into a excel file
# data_path = os.path.abspath('./Data')
# events_path = os.path.abspath('../events.xlsx')
# get_events.events2df(data_path,events_path)
# data_processing.main()
