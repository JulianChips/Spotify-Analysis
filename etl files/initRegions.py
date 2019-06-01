import charts
import pandas as pd
from tqdm import tqdm
# regions = ['ar', 'at', 'au', 'be', 'bg', 'bo', 'br', 'ca', 'ch', 'cl', 'co', 'cr', 'cz', 'de', 'dk', 'do', 'ec', 'ee', 'es', 'fi', 'fr', 'gb', 'gr', 'gt', 'hk', 'hn', 'hu', 'id', 'ie', 'il', 'in', 'is', 'it', 'jp', 'lt', 'lu', 'lv', 'mt', 'mx','my', 'ni', 'nl', 'no', 'nz', 'pa', 'pe', 'ph', 'pl', 'pt', 'py', 'ro', 'se', 'sg', 'sk', 'sv', 'th', 'tr', 'tw', 'us', 'uy', 'vn']
regions = {
	'ar':'Argentina',
	'at':'Austria',
	'au':'Australia',
	'be':'Belgium',
	'bg':'Bulgaria',
	'bo':'Bolivia',
	'br':'Brazil',
	'ca':'Canada',
	'ch':'Switzerland',
	'cl':'Chile',
	'co':'Colombia',
	'cr':'Costa Rica',
	'cz':'Czech Republic',
	'de':'Germany',
	'dk':'Denmark',
	'do':'Dominican Republic',
	'ec':'Ecuador',
	'ee':'Estonia',
	'es':'Spain',
	'fi':'Finland',
	'fr':'France',
	'gb':'United Kingdom',
	'gr':'Greece',
	'gt':'Guatemala',
	'hk':'Hong Kong',
	'hn':'Honduras',
	'hu':'Hungary',
	'id':'Indonesia',
	'ie':'Ireland',
	'il':'Israel',
	'in':'India',
	'is':'Iceland',
	'it':'Italy',
	'jp':'Japan',
	'lt':'Lithuania',
	'lu':'Luxembourg',
	'lv':'Latvia',
	'mt':'Malta',
	'mx':'Mexico',
	'my':'Malaysia',
	'ni':'Nicaragua',
	'nl':'Netherlands',
	'no':'Norway',
	'nz':'New Zealand',
	'pa':'Panama',
	'pe':'Peru',
	'ph':'Philippines',
	'pl':'Poland',
	'pt':'Portugal',
	'py':'Paraguay',
	'ro':'Romania',
	'se':'Sweden',
	'sg':'Singapore',
	'sk':'Slovakia',
	'sv':'El Salvador',
	'th':'Thailand',
	'tr':'Turkey',
	'tw':'Taiwan',
	'us':'United States',
	'uy':'Uruguay',
	'vn':'Vietnam',
	'za':'South Africa'
}
start_date = '2016-12-29'
end_date = '2019-05-16'
frequency = 'weekly'

all_charts = []
for region in regions.keys():
	print(regions.get(region))
	chart = charts.get_charts(start_date, end_date, freq=frequency, region=region, sleep=0)
	chart['region']=regions.get(region)
	chart['region_abbr']=region
	all_charts.append(chart)

pd.concat(all_charts).to_csv("allRegions.csv")