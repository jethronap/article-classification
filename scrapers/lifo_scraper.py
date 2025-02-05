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

    print("test");

    # List with queries
    desired_queries = ['efood']

    link_results = []
    article_results = []
    title_results = []

    page = 0
    # Scrape for links in website database given the queries
    for query in desired_queries:
        # Scraπe n pages
        for i in range(1):
            page = page+i
            
            soup = create_soup_from_url(url='https://www.lifo.gr/search?keyword=' + quote(query) + '&page=' + str(page))
            
            # Extracting number of link_results
            search = soup.find_all('div', attrs={'class':'container p-0'})
            
            # Search for articles within given tag:
            for s in  search:
                articles = soup.find_all('article', attrs={'class': 'row no-gutters mb-4 mb-lg-6'})
                
                # Extract the link of each article:
                for a in articles:
                    links = a.contents[1].get('href')
                    # print(links)  
                    link_results.append(links)

    # Scrape inside individual search results
    for i in range(len(link_results)):
        
        soup = create_soup_from_url(url=link_results[i])

        # Get article body and individual paragraphs within
        try:
            article_body = soup.find('div', attrs={'class':'article__body'}).findAll('p', recursive=False)
        except:
            continue

        list_paragraphs = []
        for paragraph in article_body:

            list_paragraphs.append(paragraph.text)
            complete_article = " ".join(list_paragraphs)
            
        article_results.append(complete_article)    
        
        # Get article title
        try:
            article_title = soup.find('div', attrs={'class':'article__header'}).find('h1', recursive=False)
            title_results.append(article_title.text)
        except:
            article_title = 'N/A'
            title_results.append(article_title)
        
    # Add articles and titles to pandas dataframe
    articles_list = {'Article': article_results, 'Title': title_results, 'Date Scraped': datetime.now()}
    articles_df = pd.DataFrame(data=articles_list)
    cols = ['Article', 'Title', 'Date Scraped']
    articles_df = articles_df[cols]
    # Check for duplicates in df:
    # articles_df = articles_df[articles_df.duplicated()]
    # Drop duplicates in df:
    articles_df = articles_df.drop_duplicates()
    print(articles_df);
    articles_df.to_csv(r'data/test_lifo_articles.txt', index=False, sep=' ', header=False)


    # A couple of development sanity checks:
    print(link_results)
    print(len(link_results))

    # Check if link_results are unique:
    if len(link_results) > len(set(link_results)):
        print("not unique")
    else:
        print("unique") 

    print(articles_df)

if __name__ == '__main__':
    main()