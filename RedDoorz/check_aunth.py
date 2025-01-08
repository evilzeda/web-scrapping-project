import xlsxwriter
import requests
from datetime import datetime
import json
import os
import sys

now = datetime.now()
# dt_string = now.strftime("%d%m%y")
dt_string = 'data'
dirSource = 'raw'
dirSource1 = 'reddoorz'
dirName = dirSource+'/'+dirSource1+'/' + dt_string + '/'

if not os.path.exists(dirSource):
    os.mkdir(dirSource)
if not os.path.exists(dirSource+'/'+dirSource1):
    os.mkdir(dirSource+'/'+dirSource1)
if not os.path.exists(dirName):
    os.mkdir(dirName)

# Set your authorization token here
authorization = 'Bearer 2XvZjnpOdW0lFt1l5utMuZ0NBgHHZyy-z5cugEAbzZw'  # Replace with your actual token
# authorization = 'Bearer ' + sys.argv[1]

print(authorization)

def getSiteSettings():
    headers = {
        'authority': 'd3i0gjdlegbll.cloudfront.net',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    }

    params = (
        ('locale', 'en'),
        ('domain_name', 'indonesia'),
        ('timestamp', timestamp),
        ('device_type', 'web'),
    )

    response = requests.get('https://d3i0gjdlegbll.cloudfront.net/api/v12/site_settings', headers=headers, params=params)

    with open("raw/reddoorz/" + dt_string + "/" + 'reddoorz_site_settings.json', "w", encoding='utf-8') as text_file:
        text_file.write('{"timestamp":'+timestamp+","+response.text[1:])

    return response.text

def to_excel(list, output):
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(list):
            worksheet.write_row(row_num, 0, data)

def getHotelList(json_text):
    result = [['repeated_id', 'id','country','area','name','slug', 'latitude', 'longitude', 'address', 'Reddoorz','KoolKost', 'Sans', 'No Brand', 'Indonesia']]
    jtext = json.loads(json_text)
    list = jtext['hotels_list']
    i = 0
    for l in list:
        slug = l[1]
        slug_list = str(slug).split('/')
        country = slug_list[0]
        area = slug_list[1]
        indonesia = ""
        if country.lower() == 'indonesia': indonesia = 1
        reddoorz = ""
        if str(l[0]).lower().find('reddoorz') > -1 and country.lower() == 'indonesia': reddoorz = 1
        koolkost = ""
        if str(l[0]).lower().find('koolkost') > -1 and country.lower() == 'indonesia': koolkost = 1
        sans = ""
        if str(l[0]).lower().find('sans ') > -1 and country.lower() == 'indonesia': sans = 1
        no_brand = ""
        if not (reddoorz == 1 or koolkost == 1 or sans == 1): no_brand = 1
        i=i+1
        print(i,slug)
        (repeated_id, id, latitude, longitude, address) = getDetail(slug)
        result.append([repeated_id, id, country,area,str(l[0]).strip(),'https://www.reddoorz.com/id-id/hotel/'+slug, latitude, longitude, address, reddoorz, koolkost, sans, no_brand, indonesia])
    to_excel(result, 'raw/reddoorz/reddoorz_kost_' + dt_string + '.xlsx')

f = open("raw/reddoorz/list.txt", "r")
text = f.read()
text_find = '<a href="#">'
index = text.find(text_find)
text = text[index+len(text_find):]
list = []
i = 0
while True:
    i = i+1
    index = text.find(text_find)
    if index < 0:
        break
    list.append(text[0:index])
    text = text[index+len(text_find):]
list_city = [['city','property']]
for l in list:
    text_find = ','
    index = l.find(text_find)
    city = l[0:index]
    text_find = 'ng-bind="cit.hotels_text">'
    index = l.find(text_find)
    if index < 0:
        property = 0
    else:
        property = l[index+len(text_find):index+len(text_find)+10]
        text_find = '+'
        index = property.find(text_find)
        property = property[0:index]
    if [city, int(property)] not in list_city:
        list_city.append([city, int(property)])
to_excel(list_city, 'raw/reddoorz/reddoorz_area_list_' + dt_string + '.xlsx')

def getDetail(slug):
    slug = str(slug).split('/')[-1]

    headers = {
        'authority': 'redsearch.reddoorz.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'authorization': authorization,
        'sec-ch-ua-mobile': '?0',
        'encoding': 'gzip',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://www.reddoorz.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.reddoorz.com/',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'if-none-match': 'W/"ba672d1233c9ca2907d82f9171e77687"',
    }

    params = (
        ('currency', 'IDR'),
        ('locale', 'id'),
    )

    response = requests.get('https://redsearch.reddoorz.com/api/v1/hotel/'+slug, headers=headers,
                            params=params)

    with open("raw/reddoorz/" + dt_string + "/" + slug + '.json', "w", encoding='utf-8') as text_file:
        text_file.write(response.text)

    if response.text.find('"status":404') >=0 :
        return ('0', '', '0.0', '0.0', 'Properti tidak tersedia, silakan pilih properti lain')

    jtext = json.loads(response.text)
    if jtext['repeated_ids'] == None:
        repeated_ids = 0
    else:
        repeated_ids = jtext['repeated_ids']
    
    if jtext['id'] == None:
        id = 0
    else:
        id = jtext['id']

    if jtext['latitude'] == None:
        latitude = 0
    else:
        latitude = jtext['latitude']

    if jtext['longitude'] == None:
        longitude = 0
    else:
        longitude = jtext['longitude']

    if jtext['street1'] == None:
        street1 = ''
    else:
        street1 = jtext['street1']

    if jtext['street2'] == None:
        street2 = ''
    else:
        street2 = jtext['street2']

    address = street1 + ', '+ street2

    return (repeated_ids, id, latitude, longitude, address)

def countrylist():
    import requests

    headers = {
        'authority': 'api.reddoorz.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'authorization': 'Bearer 7fe89a4ba52784f592bd30ba75ede6f668bf8527bf94c3a299f238c4dd92ed5c',
        'sec-ch-ua-mobile': '?0',
        'encoding': 'gzip',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://www.reddoorz.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.reddoorz.com/',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    }

    response = requests.get('https://api.reddoorz.com/api/v14/country_list', headers=headers)


if __name__ == '__main__':
    hotel_list = getSiteSettings()
    getHotelList(hotel_list)

