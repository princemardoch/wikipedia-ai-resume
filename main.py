import sys
import time

import requests
from groq import Groq
from bs4 import BeautifulSoup

from config import Config

groq_api_key = Config.API_KEY.groq_api_key
instruction = Config.instruction_system.instruction
urls_lists_file = Config.files.articles_urls_list

client = Groq(api_key=groq_api_key)


def get_articles_urls_list():
    with open(urls_lists_file, 'r') as files:
        urls_list = [url.strip() for url in files.readlines()]
    return urls_list

def none_valide_articles(url, status_code):
    ''' Write in a file that the URL scraping failed '''
    with open('not_scrapping.txt', 'a') as file:
        file.write(f'{url} - Status code : {status_code} \n {'------------\n'}')

def get_article(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=False)
        status_code = response.status_code

        if status_code != 200:
            print(f"Status code of '{url}' = {status_code}")
            none_valide_articles(url, status_code)
            return None
        
        content = response.content
        html = BeautifulSoup(content, 'html.parser')

        article = html.find('body').text

        print(f'Success article get - url {url}')

        return article
    except Exception as e:
        none_valide_articles(url, e)


def groq(articles):
    if articles is None:
        return None
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": articles}
        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content

def save_resume(resume, url):
    if resume is None:
        return None

    with open('articles_resume.txt', 'a') as w:
        w.write(f'url = {url}{'\n'*2}{'-'*10}\n{resume} {'\n'*2} {'-'*50}{'\n'*2}')
        
    print(f'Url = {url} : SUCCESS WRITE')
    return 'Success wirte'

if __name__ == "__main__":
    articles_urls = get_articles_urls_list()
    for url in articles_urls:
        raw_article = get_article(url)
        article_resume = groq(raw_article)
        save_resume(article_resume, url)
        time.sleep(20)
    print('\n\n FINISH')