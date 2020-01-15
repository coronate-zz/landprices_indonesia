import pandas as pd
import numpy as np
from tqdm import tqdm
import webscrape_script as wss
from datetime import date

df_urls = pd.read_csv("Input/urls_scrape.csv")
try:
    df_data = pd.read_csv("Output/data.csv")
except Exception as e:
    df_data = pd.DataFrame()

# The process is executed in two stages. In the first stage we load all the content and save it into
# HTMML file. In the second Stage we perform the webscraping on the downloaded html. This makes eassier
# the webscraping process and avoid problems with the internet connection.


def update_urlfile(df_urls, index_row):
    """
    After downloading html or scraping content the process status has to be updated.
    """
    df_urls.loc[index] = index_row
    df_urls.to_csv("Input/urls_scrape.csv", index=False)


for index in tqdm(range(len(df_urls))):
    index_row = df_urls.loc[index]
    territory = df_urls
    if index_row["status"] != True:
        url = index_row["url"]
        if index_row["html_loaded"] != True:
            print("\t\tFIRST STAGE: Load info + dowload html")
            html_name = "htmls/" + url.split("/")[-1] + ".html"
            wss.load_all_content(url, html_name, 30, 7)

            # Update  html download process stautus
            today_date = date.today()
            today_date = today_date.strftime("%d/%m/%Y")
            index_row["scrap_date"] = today_date
            index_row["html_loaded"] = True
            index_row["html_name"] = html_name

            update_urlfile(df_urls, index_row)

        else:
            html_name = index_row["html_name"]

        print("\t\tSECOND STAGE: Scrape")
        df_scrape = wss.scrape_olx(html_name, url)

        if len(df_data) == 0:
            df_data = df_scrape
        else:
            df_data = df_data.append(df_scrape)
        df_data["territory"] = territory
        df_data.to_csv("Output/data.csv")
        # Update  webscrape process stautus
        index_row["number_obs"] = df_scrape.shape[0]
        index_row["status"] = True
        update_urlfile(df_urls, index_row)

    else:
        print("\turl {} has been downloaded and scraped".format(
            index_row["url"]))
