import requests
from bs4 import BeautifulSoup

headers = {
   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

url = 'https://www.espn.com/mlb/team/_/name/tex/texas-rangers'

response = requests.get(url, headers=headers)

if(response.status_code == 200):
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        a = article.find('a')

        if a and 'href' in a.attrs:
            print(a['href'])
else:
    print("Failed to retrieve page")