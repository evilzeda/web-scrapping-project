import pandas as pd
from datetime import datetime
import requests
import json
import xlsxwriter

#
file_level = 'sheet3__.xlsx'
id_location = pd.read_excel(file_level)[["id","name"]].values.tolist()
output = 'olx_result_'+ datetime.now().strftime("%d%m%y") +'.xlsx'
result = [['url', 'id', 'user_id', 'location_region', 'location_city', 'location_district', \
           'title', 'price', 'alamat', 'latitude', 'longitude', 'kamar_mandi', 'fasilitas', 'luas_bangunan', 'description']]

def getPage(location = 1000001, page = 0):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'category': '4833',
        'facet_limit': '1000',
        'location': str(location),
        'location_facet_limit': '200',
        'page': str(page),
        'platform': 'web-desktop',
        'sorting':'desc-price',
        'user': '',
    }

    response = requests.get('https://www.olx.co.id/api/relevance/v2/search', params=params, headers=headers)

    return response

def to_excel(list,output):
    with xlsxwriter.Workbook(output) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(list):
            worksheet.write_row(row_num, 0, data)

def readPrevListingId(output_previous):
    data = pd.read_excel(output_previous)
    list_id = data["id"]
    list_id.drop_duplicates(inplace=True)
    return list_id.values.tolist()

def getListingInformation(jsonLoads):
    try:
        id = jsonLoads["id"]
        description = jsonLoads["description"]
        title = jsonLoads["title"]
        price = str(jsonLoads["price"]["value"]["display"]).replace('Rp','').replace('.','').replace(' ','')
        location_region = jsonLoads["locations_resolved"]["ADMIN_LEVEL_1_name"]
        location_city = jsonLoads["locations_resolved"]["ADMIN_LEVEL_3_name"]
        location_district = jsonLoads["locations_resolved"]["SUBLOCALITY_LEVEL_1_name"]
        user_id = jsonLoads["user_id"]
        parameters = jsonLoads["parameters"]
        luas_bangunan = 0
        kamar_mandi = 0
        fasilitas = []
        alamat = ""
        for param in parameters:
            if param["key"] == "p_sqr_building":
                luas_bangunan = param["value"]
            if param["key"] == "p_bathroom":
                kamar_mandi = param["value"]
            if param["key"] == "p_facility":
                if "values" in param:
                    [fasilitas.append(f["value"]) for f in param["values"]]
            if param["key"] == "p_alamat":
                alamat = param["value"]
        fasilitas = ','.join(fasilitas)
        latitude = jsonLoads["locations"][0]["lat"]
        longitude = jsonLoads["locations"][0]["lon"]

        return ['https://www.olx.co.id/item/'+str(id), str(id), user_id, location_region, location_city, location_district, title, price, \
                alamat, latitude, longitude, kamar_mandi, fasilitas, luas_bangunan, description]
    except Exception:
        print('Error','https://www.olx.co.id/item/'+str(id))
        return ['https://www.olx.co.id/item/'+str(id), str(id), '', '', '', '', '', 0, \
                '', 0, 0, 0, '', 0, '']

def scrapListing(output_previous = '',continue_location = '',continue_page = 0):
    global id_location
    id_clean = []
    for location in id_location:
        page = -1
        if output_previous != '':
            if location[1] == continue_location:
                page = continue_page
                id_clean = readPrevListingId(output_previous)
                output_previous = ''
        while output_previous == '':
            page+=1
            while True:
                print(location[0],location[1],page, datetime.now())
                scrape = getPage(location[0],page).text
                try:
                    jsontext = json.loads(scrape)
                    break
                except Exception:
                    print("getPage error. Re-scrape")
                    continue
            if "data" not in jsontext:
                break
            if len(jsontext["data"]) == 0:
                break
            total_duplicate = 0
            for listing in jsontext["data"]:
                kost = getListingInformation(listing)
                id = int(kost[1])
                if id not in id_clean:
                    id_clean.append(id)
                    result.append(kost)
                    print(f'{kost}, success scrap')
                    to_excel(result,output)
                else:
                    total_duplicate+=1
            if total_duplicate>1:
                print('total_duplicate',total_duplicate)

def main():
    global output
    # new scrape: scrapListing()
    scrapListing()
    # continue scrape, for example: scrapListing('olx_result_060323.xlsx', 'palmerah', 15)
    # scrapListing(output, 'palmerah', 15)

if __name__ == '__main__':
    main()