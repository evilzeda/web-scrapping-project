import re
import traceback
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import re
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date, timedelta

import pandas as pd

edge_driver_path = './msedgedriver.exe'

def scrap(site: str, edge_driver_path: str) -> int:
    print(site, '- Processing')

    regex = re.compile(pattern=r'[^0-9]')

    options = Options()
    options.add_argument("--headless")
    #options.add_argument("--start-maximized")  # Maximize the browser window
    #options.add_argument("--inprivate")  # Open an in-private browsing session

    driver = webdriver.Edge(
        executable_path=edge_driver_path,
        options=options
    )
    df2 =pd.DataFrame()

    try:
        driver.get('https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831')

        #last_page_elem = driver.find_element_by_xpath("/html/body/div[3]/section/div[4]/div/div[1]/div/nav/ul/li[10]/a").get_attribute("data-homeypagi")
        last_page_elem = driver.find_element(By.XPATH, "/html/body/div[3]/section/div[4]/div/div[1]/div/nav/ul/li[10]/a").get_attribute("data-homeypagi")
        nums_of_page = re.sub(
            pattern=regex,
            repl='',
            string=last_page_elem
        )

        driver.get('https://infokost.id/search-results/page/' + nums_of_page + '/')
        #listing_count_last_page = driver.find_elements_by_class_name(name='item-media-price')
        listing_count_last_page = driver.find_elements(By.CLASS_NAME, 'item-media-price')

        listing_count = len(listing_count_last_page)

        total_listing = ((int(nums_of_page)-1)*16)+listing_count
        print(nums_of_page)

        
        for p in range(1, int(nums_of_page)):
            print("p---",p)
            link1='https://infokost.id/search-results/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'
            link2='https://infokost.id/search-results/page/{}/?location_search=Jakarta+Pusat%2C+Central+Jakarta+City%2C+Jakarta%2C+Indonesia&search_city=central-jakarta&search_area=central-jakarta-city&search_country=indonesia&lat=-6.1805113&lng=106.8283831'.format(p)
            print(link2)
            if p==1:
                print("p1")
                driver.get(link1)
            else:
                print("p2")
                driver.get(link2)

            element=driver.find_elements(By.XPATH, '//div[@class="item-wrap infobox_trigger homey-matchHeight"]/div/div[2]/div[1]/div/h2/a')
            link_properti_list_ind=[]
            for i in element:
                i_href=i.get_attribute('href')
                # print(i_href)
                link_properti_list_ind.append(i_href)
            
            for l in  (link_properti_list_ind):
                print(l)
                driver.get(l)
                #agar web load sempurna
                time.sleep(3)

                #namaproperti
                properti=driver.find_element(By.XPATH, '//*[@id="section-body"]/section[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/h1')
                properti_text=properti.text
                print(properti_text)

                #address_properti
                address=driver.find_element(By.XPATH, '//*[@id="section-body"]/section[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/div/address')
                address_text=address.text
                print(address_text)

                #jenis kost 
                jenis=driver.find_element(By.XPATH, '//*[@id="section-body"]/section[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[1]/div[4]/strong')
                jenis_text=jenis.text
                print(jenis_text)
                
                #fasilitas gedung
                fasilitas=driver.find_elements(By.XPATH, '//*[@id="features-section"]/div/div/div/div[2]/ul[1]/li')
                fasilitas_list=[f.text for f in fasilitas]
                fasilitas_join = "; ".join([str(item) for item in fasilitas_list if item])
                print("fasilitas gedung: ",fasilitas_join)

                #kamar
                room=driver.find_elements(By.XPATH, '//*[@id="similar-listing-section"]/div[@class="item-row item-list-view"]/div')
                for item in room:
                    
                    room_listing=item.find_element(By.CSS_SELECTOR, ' div > div.media-body.item-body.clearfix > div.item-title-head.table-block > div > h2')
                    room_listing_text=room_listing.text
                    print(room_listing)


                    #add here for other info about room ------------------->

                    
                
                    dict1={"link_properti": l, "alamat": address_text,
                        "nama_properti":properti_text, "jenis_kost":jenis_text, "fasilitas_gedung":fasilitas_join, "tipe_kamar":room_listing_text,
                        "room_listing": room_listing,
                            "harga_room_listing":"",
                            }

                    df_dict1 = pd.DataFrame([dict1])
                    df2 = pd.concat([df2, df_dict1], ignore_index=True)

        driver.quit()
        df2.to_csv(f"infokost_details.csv", index=False, sep=',')

    except Exception:
        print(site, '- Exception occurred')
        traceback.print_exc()
        total_listing = 0
        listing_count = 0
        print(site, '- Failed')

    print(site, '- Done')

    return total_listing

scrap('infokost', edge_driver_path)