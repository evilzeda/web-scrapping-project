import re
import traceback
import csv
import numpy as np
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.edge.options import Options
import re
import traceback
import time
# from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.edge.service import Service             # using Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, timedelta

import pandas as pd

# driver_path='driver/geckodriver'
# driver_path = 'driver/chromedriver'
driver_path = 'driver/msedgedriver.exe'
serviceEdge = Service(driver_path)

edge_options = Options()
edge_options.add_argument("--headless") 
edge_options.add_argument('--disable-gpu')
edge_options.add_argument('--log-level=3')  ## only display log (WARN, ERROR, FATAL)

info_listing=[["id","link","name","address"]]
def scrap(site: str, driver_path: str) -> int:
    print(site, '- Processing')

    # URL_TARGET =  'https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Jakarta%2C%20Indonesia&search_city&search_area&search_country=indonesia&lat=-6.2087634&lng=106.845599'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
    # URL_TARGET = 'https://infokost.id/search-results/'
    URL_TARGET = 'https://infokost.id/search-results/?location_search=Bandung%2C+Bandung+City%2C+West+Java%2C+Indonesia&search_city=bandung&search_area=bandung-city&search_country=indonesia&lat=-6.9174639&lng=107.6191228'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Jogja%2C+Yogyakarta+City%2C+Special+Region+of+Yogyakarta%2C+Indonesia&search_city=yogyakarta&search_area=yogyakarta-city&search_country=indonesia&lat=-7.7955798&lng=110.3694896'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Surabaya%2C+East+Java%2C+Indonesia&search_city=surabaya&search_area=kota-sby&search_country=indonesia&lat=-7.2574719&lng=112.7520883'
    # URL_TARGET = 'https://infokost.id/search-results/?location_search=Denpasar%2C+Denpasar+City%2C+Bali%2C+Indonesia&search_city=denpasar&search_area=denpasar-city&search_country=indonesia&lat=-8.670458199999999&lng=115.2126293'

    regex = re.compile(pattern=r'[^0-9]')

    driver = webdriver.Edge(
            # executable_path=driver_path,
            service = serviceEdge,
            options = edge_options
        )

    df2 =pd.DataFrame()
    try:    
        # driver.get(URL_TARGET)
        # driver.get('https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831&radius=10')
        # driver.get('https://infokost.id/search-results/?location_search=Jakarta%2C%20Indonesia&search_city&search_area&search_country=indonesia&lat=-6.2087634&lng=106.845599&radius=20')
        # driver.get('https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321&radius=5')
        # driver.get('https://infokost.id/search-results/')
        driver.get('https://infokost.id/search-results/?location_search=Bandung%2C+Bandung+City%2C+West+Java%2C+Indonesia&search_city=bandung&search_area=bandung-city&search_country=indonesia&lat=-6.9174639&lng=107.6191228&radius=20')
        # driver.get('https://infokost.id/search-results/?location_search=Jogja%2C+Yogyakarta+City%2C+Special+Region+of+Yogyakarta%2C+Indonesia&search_city=yogyakarta&search_area=yogyakarta-city&search_country=indonesia&lat=-7.7955798&lng=110.3694896&radius=10')
        # driver.get('https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321&radius=10')
        # driver.get('https://infokost.id/search-results/?location_search=Surabaya%2C+East+Java%2C+Indonesia&search_city=surabaya&search_area=kota-sby&search_country=indonesia&lat=-7.2574719&lng=112.7520883&radius=10')
        # driver.get('https://infokost.id/search-results/?location_search=Denpasar%2C+Denpasar+City%2C+Bali%2C+Indonesia&search_city=denpasar&search_area=denpasar-city&search_country=indonesia&lat=-8.670458199999999&lng=115.2126293&radius=5')
        last_page_elem = driver.find_element(By.XPATH, "/html/body/div[3]/section/div[4]/div/div[1]/div/nav/ul/li[10]/a").get_attribute("data-homeypagi")
        listing_count_last_page = driver.find_elements(By.CLASS_NAME, 'item-media-price')
        listing_count = len(listing_count_last_page)

        nums_of_page = re.sub(
                    pattern=regex,
                    repl='',
                    string=last_page_elem
                )

        # for p in range(1, int(nums_of_page)):
        for p in range(1, int(nums_of_page)):
        # for p in range(1):  ## for testing purpose
            # link1='https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'.format(p)
            # link1='https://infokost.id/search-results/?location_search=Jakarta%2C%20Indonesia&search_city&search_area&search_country=indonesia&lat=-6.2087634&lng=106.845599'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Jakarta%2C%20Indonesia&search_city&search_area&search_country=indonesia&lat=-6.2087634&lng=106.845599'.format(p)
            # link1='https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Malang%2C%20Malang%20City%2C%20East%20Java%2C%20Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'.format(p)
            link1='https://infokost.id/search-results/?location_search=Bandung%2C+Bandung+City%2C+West+Java%2C+Indonesia&search_city=bandung&search_area=bandung-city&search_country=indonesia&lat=-6.9174639&lng=107.6191228'
            link2='https://infokost.id/search-results/page/{}/?location_search=Bandung%2C%20Bandung%20City%2C%20West%20Java%2C%20Indonesia&search_city=bandung&search_area=bandung-city&search_country=indonesia&lat=-6.9174639&lng=107.6191228'.format(p)
            # link1='https://infokost.id/search-results/?location_search=Jogja%2C+Yogyakarta+City%2C+Special+Region+of+Yogyakarta%2C+Indonesia&search_city=yogyakarta&search_area=yogyakarta-city&search_country=indonesia&lat=-7.7955798&lng=110.3694896'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Jogja%2C%20Yogyakarta%20City%2C%20Special%20Region%20of%20Yogyakarta%2C%20Indonesia&search_city=yogyakarta&search_area=yogyakarta-city&search_country=indonesia&lat=-7.7955798&lng=110.3694896'.format(p)
            # link1='https://infokost.id/search-results/?location_search=Malang%2C+Malang+City%2C+East+Java%2C+Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
            # link2='https://infokost.id/search-results/page/2/?location_search=Malang%2C%20Malang%20City%2C%20East%20Java%2C%20Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
            # link3='https://infokost.id/search-results/page/2/?location_search=Malang%2C%20Malang%20City%2C%20East%20Java%2C%20Indonesia&search_city=malang&search_area=malang-city&search_country=indonesia&lat=-7.9666204&lng=112.6326321'
            # link1='https://infokost.id/search-results/?location_search=Surabaya%2C+East+Java%2C+Indonesia&search_city=surabaya&search_area=kota-sby&search_country=indonesia&lat=-7.2574719&lng=112.7520883'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Surabaya%2C%20East%20Java%2C%20Indonesia&search_city=surabaya&search_area=kota-sby&search_country=indonesia&lat=-7.2574719&lng=112.7520883'.format(p)
            # link1='https://infokost.id/search-results/?location_search=Denpasar%2C+Denpasar+City%2C+Bali%2C+Indonesia&search_city=denpasar&search_area=denpasar-city&search_country=indonesia&lat=-8.670458199999999&lng=115.2126293'
            # link2='https://infokost.id/search-results/page/{}/?location_search=Denpasar%2C%20Denpasar%20City%2C%20Bali%2C%20Indonesia&search_city=denpasar&search_area=denpasar-city&search_country=indonesia&lat=-8.670458199999999&lng=115.2126293'.format(p)
            # link1='https://infokost.id/search-results/'
            # link2='https://infokost.id/search-results/page/{}'.format(p)

            if p==1:
                driver.get(link1)
            # elif p==2:
            #     driver.get(link2)
            # elif p==3:
            #     driver.get(link3)
            else:
                # print('')
                driver.get(link2)
            LISTING_PARENTS = '//div[@class="item-wrap infobox_trigger homey-matchHeight"]' 
            # LISTING_CARD = '//div[@class="item-wrap infobox_trigger homey-matchHeight"]/div/div[2]/div[1]/div/h2/a'
            # LISTING_CARD = '//div[@class="item-wrap infobox_trigger homey-matchHeight"]'
            element = driver.find_elements(By.XPATH, LISTING_PARENTS)

            link_properti_list_ind=[]
            for i in element:
                i_id = i.get_attribute('data-id')
                listing_name = i.find_element(By.CLASS_NAME,'title')
                LISTING_CARD = i.find_element(By.CLASS_NAME,'hover-effect')
                i_href = LISTING_CARD.get_attribute('href')
                # i_name = LISTING_CARD.get_text()
                i_name = listing_name.find_element(By.XPATH,'a').text
                listing_address = i.find_element(By.CLASS_NAME,'item-address').text
                info_listing.append([i_id,i_href,i_name, listing_address])
            print(info_listing) 
            file = open(r'20231110bandung.csv', 'w+', newline ='')
            with file:
                write = csv.writer(file)
                write.writerows(info_listing)      
            for l in  link_properti_list_ind:
                # l = link_properti_list_ind[1] ## for testing purpose: sampling Kost Omah Ciragil 37
                time.sleep(3)
                driver.get(l) 
                print(l)
                ITEM_CARD = "//div[@class='title-section']"
                # FACILITY_GEDUGN_SECTION = "//div[@id='features-section']"
                # TIPE_KAMAR_SECTION = "//div[contains(@class, 'room-type-sec')]"

                wait = WebDriverWait(driver, 10)

                #namaproperti
                try:
                    properti_text = wait.until(EC.presence_of_element_located((By.XPATH, ITEM_CARD + "//h1[@class='listing-title']"))).text
                    properti_text = properti_text.strip()  
                except:
                    properti_text = ''        
                # print(properti_text)
                #address_properti
                try:
                    address_text= wait.until(EC.presence_of_element_located((By.XPATH, ITEM_CARD + "//address[@class='item-address']"))).text
                except:
                    address_text= ''
                # print(address_text)
                # area administrasi
                try:
                    area_adm = wait.until(EC.presence_of_element_located((By.XPATH, ITEM_CARD + "//address[@class='sec-address']"))).text
                    area_adm_clean = area_adm.replace('\n', '')
                    area_adm_clean = area_adm_clean.replace('\t', ' ')

                    rgx = re.compile(pattern=r'[0-9]')

                    clean_str = re.sub(
                                pattern=rgx,
                                repl='',
                                string=area_adm_clean
                            )

                    # split full text area name into each level area administration
                    split_str = clean_str.split(",")
                    kelurahan = split_str[0].strip()
                    kecamatan = split_str[1].strip()
                    kota = split_str[2].strip()
                    provinsi = split_str[3].strip()
                except:
                    area_adm = ''
                    kelurahan = ''
                    kecamatan = ''
                    kota = ''
                    provinsi = ''
                # print(area_adm)
                # print(kelurahan)
                # print(kecamatan)
                # print(kota)
                # print(provinsi)

                #gender kost
                try: 
                    jenis_text= wait.until(EC.presence_of_element_located((By.XPATH, ITEM_CARD + "//div[contains(@class, 'gender-box')]"))).text
                except:
                    jenis_text=''
                # print(jenis_text)
                #fasilitas gedung
                try:
                    fasilitas = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='features-section']//ul[1]/li")))  ## masih perlu klik fasilitas lainnya dulu baru dapet semua fasilitias
                    fasilitas_list=[f.text for f in fasilitas]
                    fasilitas_join = "-".join([str(item) for item in fasilitas_list if item])
                except:
                    fasilitas = ''
                    fasilitas_join = ''
                # print(fasilitas_join)

                #kamar
                # try:
                #rooms = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'room-type-sec')]//div[@class='media property-item ']")))
                # rooms = driver.find_elements(By.XPATH, '//*[@id="similar-listing-section"]/div[@class="item-row item-list-view"]/div')
                try:
                    rooms = driver.find_elements(By.XPATH,"//div[contains(@class, 'room-type-sec')]//div[@class='media property-item ']")
                    for room in rooms:           
                            # tipe kamar
                            try:
                                room_listing_text = room.find_element(By.XPATH, ".//h2[@class='title roomtitle']").text  # access child element dari room element
                            except:
                                room_listing_text = ''
                            # harga kamar
                            try:
                                room_price_text = room.find_element(By.XPATH, ".//span[@class='item-price']").text  # access child element dari room element
                                room_price_int = int(re.sub(r'\D', '', room_price_text))
                            except:
                                room_price_text = ''
                                room_price_int = 0
                            # luas kamar
                            try:
                                room_area_text  = room.find_element(By.XPATH, ".//address[sup]").text
                            # room_area_text  = room.find_element(By.XPATH, ".//item-address[sup]").text
                                pattern = r"\d+m2"
                                room_area = re.findall(pattern, room_area_text)[0]
                                room_area = room_area.replace('m2', '')
                                room_area_int = int(room_area)
                            except:
                                room_area_text = ''
                                room_area_int = 0
                            dict1={"link_properti": l, 
                                    "nama_properti":properti_text, 
                                    "alamat": address_text,
                                    "kelurahan": kelurahan,
                                    "kecamatan": kecamatan,
                                    "kota": kota,
                                    "provinsi": provinsi,
                                    "jenis_kost":jenis_text, 
                                    "fasilitas_gedung":fasilitas_join, 
                                    "tipe_kamar":room_listing_text,
                                    # "room_listing": room_listing,
                                    "room_area": room_area_int,
                                        "harga_room_bulanan":room_price_int
                                        }
                            df_dict1 = pd.DataFrame([dict1])
                            df2 = pd.concat([df2, df_dict1], ignore_index=True)
                except:
                    dict1={"link_properti": l, 
                                    "nama_properti":properti_text, 
                                    "alamat": address_text,
                                    "kelurahan": kelurahan,
                                    "kecamatan": kecamatan,
                                    "kota": kota,
                                    "provinsi": provinsi,
                                    "jenis_kost":jenis_text, 
                                    "fasilitas_gedung":fasilitas_join, 
                                    "tipe_kamar":'',
                                    # "room_listing": room_listing,
                                    "room_area": '',
                                        "harga_room_bulanan":0
                                        }
                    df_dict1 = pd.DataFrame([dict1])
                    df2 = pd.concat([df2, df_dict1], ignore_index=True)


        print(site, '- Success')
        # file = open(r'jakarta_pusat.csv', 'w+', newline ='')
        # with file:
        #     write = csv.writer(file)
        #     write.writerows(info_listing)
    except Exception:
        print(site, '- Exception occurred')
        traceback.print_exc()
        # total_listing = 0
        # listing_count = 0
        print(site, '- Failed')
    
    finally:
        driver.quit()
        # df2.to_csv("infokost_details_jakarta_pusat_fix.csv", index=False, sep='|')
        # file = open(r'D:\\web_scrapping\\infokost_scrap\\jakarta_pusat.csv', 'w+', newline ='')
        # with file:
        #     write = csv.writer(file)
        #     write.writerows(info_listing)

    return print(site, '- Done')

scrap('infokost', driver_path)