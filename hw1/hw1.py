#pip install wget

import urllib.request as url
import pandas as pd
import wget

wget('https://library.ucsd.edu/dc/object/bb4003017c')

url.urlretrieve('https://library.ucsd.edu/dc/object/bb4003017c','phy577_projects/data/test.csv')

data = pd.read_csv('phy577_projects/data/XXXXXX.csv')
