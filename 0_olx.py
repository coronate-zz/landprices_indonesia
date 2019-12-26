
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen


url = "https://www.olx.co.id/jambi_g2000008/tanah_c4827"
driver = webdriver.Chrome(
    "/home/alejandrocoronado/Dropbox/Github/landprices_indonesia/Drivers/chromedriver_78")
driver.get(url)
time.sleep(10)


def click_loadmore_btn():
    """
    Clicks on olx "MUAT "
    """
    loadmore_btn = driver.find_element_by_xpath(
        '//*[@class="rui-3sH3b rui-23TLR rui-1zK8h"]')
    loadmore_btn.click()

#<button type = "button" data - aut - id = "btnLoadMore" "> <span > muat lainnya < /span > < / button >


def load_all_content(name_file):
    """ This function press the load more btn until all content has been shown on the browser
    Then the function saves the information in a html file with name_file name
    """
    cont = 0
    while True:
        try:
            print("Loading: {}".format(cont))
            click_loadmore_btn()
            time.sleep(2)
            cont += 1
        except Exception as e:
            print(e)
            break

    # Sabe HTML content
    content = driver.page_source
    with open(name_file, 'w') as f:
        f.write(content)

# load_all_content("htmls/olx.html")


html_url = open(
    "/home/alejandrocoronado/Dropbox/Github/landprices_indonesia/htmls/olx.html")
#html_url = urlopen("https://www.kickstarter.com/projects/lynnemthomas/uncanny-magazine-year-6-raise-the-roof-raise-the-rates?ref=section-homepage-view-more-discovery-p1")
bsObj = BeautifulSoup(html_url)
land_offers = bsObj.findAll("li", {"data-aut-id": re.compile("itemBox")})
offer_cont = 0
df_offers = pd.DataFrame()

for element in land_offers:
    pandas_row = dict()

    element_location = element.findAll(
        "span", {"data-aut-id": re.compile("item-location")})[0].text
    element_title = element.findAll(
        "span", {"data-aut-id": re.compile("itemTitle")})[0].text
    element_price = element.findAll(
        "span", {"data-aut-id": re.compile("itemPrice")})[0].text
    element_date = element.findAll(
        "span", {"class": re.compile("zLvFQ")})[0].text

    print("\n\nTEST: \n\telement_title {}\n\telement_location: {}\n\telement_price: {}\n\telement_date: {} ".format(
        element_title, element_location, element_price, element_date))

    pandas_row["title"] = element_title
    pandas_row["price"] = element_price
    pandas_row["location"] = element_location
    pandas_row["date"] = element_date

    pandas_row = pd.DataFrame(pandas_row, index=[offer_cont])
    offer_cont += 1
    # SAVE INFO with whole information of pledges (one observation per pledge per project)
    if len(df_offers) == 0:
        df_offers = pandas_row
    else:
        df_offers = df_offers.append(pandas_row)


array(['13 Des', '12 Des', '11 Des', '10 Des', '09 Des', '16 Nov',
       '12 Sep', '7 hari yang lalu', '18 Des', 'Hari ini', 'Kemarin',
       '3 hari yang lalu', '4 hari yang lalu', '07 Des',
       '5 hari yang lalu', '6 hari yang lalu', '17 Des', '16 Des',
       '15 Des', '14 Des', '08 Des', '06 Des', '05 Des', '04 Des',
       '03 Des', '02 Des', '01 Des', '30 Nov', '29 Nov', '28 Nov',
       '27 Nov', '26 Nov', '25 Nov', '24 Nov', '23 Nov', '22 Nov',
       '21 Nov', '20 Nov', '19 Nov', '18 Nov', '17 Nov', '15 Nov',
       '14 Nov', '13 Nov', '12 Nov', '11 Nov', '10 Nov', '09 Nov',
       '08 Nov', '07 Nov', '06 Nov', '05 Nov', '04 Nov', '03 Nov',
       '02 Nov', '01 Nov', '31 Okt', '30 Okt', '29 Okt', '28 Okt',
       '27 Okt', '26 Okt', '25 Okt', '24 Okt', '23 Okt', '22 Okt',
       '21 Okt', '20 Okt', '19 Okt', '18 Okt', '17 Okt', '16 Okt',
       '15 Okt', '14 Okt', '13 Okt', '12 Okt', '11 Okt', '10 Okt',
       '09 Okt', '08 Okt', '07 Okt', '06 Okt', '05 Okt', '04 Okt',
       '03 Okt', '02 Okt', '01 Okt', '30 Sep', '29 Sep', '28 Sep',
       '27 Sep', '26 Sep', '25 Sep', '07 Sep', '22 Jun', '24 Mei',
       '15 Sep', '13 Sep', '30 Agu', '03 Jul'], dtype=object)
