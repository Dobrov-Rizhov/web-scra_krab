from pprint import pprint

import  requests
import bs4
import json

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
response = requests.get('https://habr.com/ru/articles/')
soup = bs4.BeautifulSoup(response.text, features='lxml')

articles_list = soup.findAll('article', class_='tm-articles-list__item')

parsed_data = []
for art in articles_list:
    link = f"https://habr.com{art.find('a', class_='tm-title__link')['href']}"
    respon = requests.get(link)
    soup = bs4.BeautifulSoup(respon.text, 'lxml')
    title = soup.find('h1').text.rstrip()
    date = soup.find('time')['title']
    text = soup.find('p').text
    for word in KEYWORDS:
        if word in text.lower():
            parsed_data.append({
                'data': date,
                'title': title,
                'link': link,
                })
        else:
            print('В этой статье нет нужных слов')

with open('pars.json', 'w') as file:
    file.write(json.dumps(parsed_data, ensure_ascii=False, indent=3))

