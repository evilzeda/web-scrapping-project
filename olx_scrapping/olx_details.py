import pandas as pd
import json
import os
import sys
import re

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

sys.path.append(os.path.abspath('..'))

from service import (
    redshift_write,
    s3_upload
)
from util import (
    parse_config,
    get_redshift_conn,
    get_s3_client
)

file_level = 'level3.xlsx'
id_location = pd.read_excel(file_level)[["id","name"]].values.tolist()
output = 'olx_result_'+ datetime.now().strftime("%Y-%m-%d") +'.json'
key = 'scraper-project/competitor-listing-details/%s' % output
result = ""

def getListing(location = 1000001, page = 0):
    url = 'https://www.olx.co.id/api/relevance/v4/search?category=4833&facet_limit=1000&location=' + str(location) + '&location_facet_limit=200&page=' + str(page) + '&platform=web-desktop&sorting=desc-price&user='

    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')

    driver = webdriver.Firefox(
        executable_path='/home/mamiteam/scraper-project/webdriver/geckodriver',
        firefox_options=firefox_options
    )

    driver.implicitly_wait(5)

    try:
        driver.get(url)

        listing = driver.find_element_by_xpath("//div[@id='json']").text

        driver.quit()
    except Exception as e:
        print(str(e))

    return listing

def processtoRedshift():
    try:
        # parse config.ini
        config = parse_config(path='../config.ini')

        # s3
        s3_client = get_s3_client(config=config)

        # redshift
        redshift_conn = get_redshift_conn(config=config)
        redshift_conn.autocommit = True
        redshift_cursor = redshift_conn.cursor()

        if s3_upload(client=s3_client, config=config, file=output, key=key):
            print('Uploaded to S3')

            # remove file after successfully uploaded
            os.remove(path=output)

            copy_command = """
                COPY scraping.olx_listing_details
                FROM 's3://mamikos-data/%s'
                CREDENTIALS 'aws_iam_role=arn:aws:iam::331500234476:role/myRedshiftRole'
                JSON 'auto' EMPTYASNULL
            """ % key

            # write to redshift
            if redshift_write(cursor=redshift_cursor, statement=copy_command):
                print('Loaded to Redshift')
            else:
                print('failed write to redshift')
        else:
            print('failed upload to s3')
    except Exception as e:
        print(str(e))

def getListingInformation(jsonLoads):
    try:
        id = jsonLoads["id"]
    except:
        id = 0
        pass
    try:
        description = jsonLoads["description"]
    except:
        description = ''
        pass
    try:
        title = jsonLoads["title"]
    except:
        title = ''
        pass
    try:
        price = str(jsonLoads["price"]["value"]["display"]).replace('Rp','').replace('.','').replace(' ','')
    except:
        price = 0
        pass
    try:
        location_region = jsonLoads["locations_resolved"]["ADMIN_LEVEL_1_name"]
    except:
        location_region = ''
        pass
    try:
        location_city = jsonLoads["locations_resolved"]["ADMIN_LEVEL_3_name"]
    except:
        location_city = ''
        pass
    try:
        location_district = jsonLoads["locations_resolved"]["SUBLOCALITY_LEVEL_1_name"]
    except:
        location_district = ''
        pass
    try:
        user_id = jsonLoads["user_id"]
    except:
        user_id = 0
        pass
    try:
        parameters = jsonLoads["parameters"]
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
    except:
        luas_bangunan = 0
        kamar_mandi = 0
        fasilitas = ''
        alamat = ''
        pass
    try:
        latitude = jsonLoads["locations"][0]["lat"]
    except:
        latitude = 0
        pass
    try:
        longitude = jsonLoads["locations"][0]["lon"]
    except:
        longitude = 0
        pass
    try:
        created_at = re.sub('T', ' ', jsonLoads["created_at"])[:19]
    except:
        created_at = ''
        pass
    scraped_at = datetime.now().strftime("%Y-%m-%d")

    return '{"url":"https://www.olx.co.id/item/'+str(id)+'", "id":'+str(id)+', "user_id":'+str(user_id)+ \
            ', "location_region":'+json.dumps(location_region)+', "location_city":'+json.dumps(location_city)+', "location_district":'+json.dumps(location_district)+ \
            ', "title":'+json.dumps(title)+', "price":'+str(price)+', "alamat":'+json.dumps(alamat)+', "latitude":'+str(latitude)+', "longitude":'+str(longitude)+\
            ', "kamar_mandi":'+str(kamar_mandi)+', "fasilitas":'+json.dumps(fasilitas)+', "luas_bangunan":'+str(luas_bangunan)+', "description":'+json.dumps(description)+\
            ', "scraped_at":'+json.dumps(scraped_at)+', "created_at":'+json.dumps(created_at)+'}'

def scrapListing():
    global output
    global result
    global id_location
    id_clean = []
    for location in id_location:
        print(location[0],location[1],datetime.now())
        page = -1
        while True:
            page+=1
            while True:
                try:
                    scrape = getListing(location[0],page)
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
                id = listing["id"]
                if id not in id_clean:
                    id_clean.append(id)
                    kost = getListingInformation(listing)
                    result += kost
                else:
                    total_duplicate+=1
            if total_duplicate>1:
                print('total_duplicate',total_duplicate)
        with open(output, 'w') as f:
            f.write(result)

def main():
    global output

    scrapListing()
    processtoRedshift()

if __name__ == '__main__':
    main()