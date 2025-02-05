from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

import pandas as pd

# Make an http query from url and create soup to parse
def create_soup_from_url (url):
    
    # To avoid 403-error using User-Agent
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    response = urllib.request.urlopen( req )
                
    html = response.read()
    
    # Parsing response
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def main():

    # List with queries
    desired_queries = ['efood']
    desired_date_start = '2021-08-01'
    desired_date_end = '2021-11-01'
    link_results = []
    article_results = []
    title_results = []

    page = 0
    # Scrape for links in website database given the queries
    for query in desired_queries:
        # Scrape n pages
        for i in range(8):
            page = page+i
                
            soup = create_soup_from_url(url='https://www.efsyn.gr/search?keywords=' + quote(query) + '&created=' + desired_date_start + '&created_1=' + desired_date_end  + '&sort_by=created&page=' + str(page))
            
            # Extracting results
            article_area = soup.find('div',class_='split-content__main')

            # Search for articles within given tag
            articles = article_area.find_all('article')
                
            # Extract the link of each article:
            for a in articles:
                links = "https://www.efsyn.gr" + a.contents[9].get('href')
                print(links)
                link_results.append(links)

if __name__ == "__main__":
    main()