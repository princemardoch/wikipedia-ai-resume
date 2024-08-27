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


def save_not_valid_url(url, error_cause):
    ''' Write in a file that the URL scraping failed '''
    with open('not_scrapping.txt', 'a') as file:
        file.write(f'{url} - Status code : {error_cause}\n{'-'*20}\n')

def get_articles_urls_list():
    with open(urls_lists_file, 'r') as files:
        urls_list = [url.strip() for url in files]
    return urls_list

def get_url_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.SSLError:
        return requests.get(url, headers=headers, verify=False)
    except Exception as e:
        save_not_valid_url(url)
        return None

def get_content(response: requests.Response):
    if not response:
        print(f'Response is {type(response)}')
        return None
    
    status_code = response.status_code

    if status_code != 200:
        print(f"Status code of '{url}' = {status_code}")
        save_not_valid_url(url, status_code)
        return None
    return response.content
    
def get_text_article(content):
    html = BeautifulSoup(content, 'html.parser')
    article = html.find('body').text

    print(f'Success article get - url {url}')
    return article


class Groq_ai:
    @staticmethod
    def resume(articles):
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

if __name__ == "__min__":
    articles_urls = get_articles_urls_list()
    for url in articles_urls:
        requests_response = get_url_response(url)
        requests_content = get_content(requests_response)
        text_article = get_text_article(requests_content)
        resume_article = Groq_ai.resume(text_article)
        save_resume(resume=resume_article)
    print('\n\n FINISH')