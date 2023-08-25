import urllib.request as url
import pandas as pd

# urllib.request.urlretrieve('https://www.ndbc.noaa.gov/view_text_file.php?filename=41025h2022.txt.gz&dir=data/historical/stdmet/','41025h2022.csv')

urllib.request.urlretrieve('https://library.ucsd.edu/dc/object/bb4003017c','phy577_projects/data/test.csv')

url.urlretrieve('https://library.ucsd.edu/dc/object/bb4003017c','phy577_projects/data/test.csv')
