from bs4 import BeautifulSoup as bs
from time import sleep, perf_counter
from requests_html import AsyncHTMLSession, HTMLSession
import asyncio
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

searchResults = []

def tj_search(query):
  baseurl = "https://www.traderjoes.com"
  url = f'{baseurl}/home/search?q={query}&section=products&global=yes'
  response = selenium_render_page(url)
  soup = bs(response, 'html.parser')
  results = soup.find_all(class_='SearchResultCard_searchResultCard__3V-_h')

  # print('Trader Joe\'s')
  for item in results[:10]:
    dict = {
      'name': item.h3.text,
      'price': float(item.find(class_='ProductPrice_productPrice__price__3-50j').text[1:]),
      'size': item.find(class_='ProductPrice_productPrice__unit__2jvkA').text[1:],
      'store': 'Trader Joe\'s'
    }
    searchResults.append(dict)
    # print(dict)


def albert_search(query):
  baseurl = 'https://www.albertsons.com/'
  url = f'{baseurl}/shop/search-results.html?q={query}'
  response = selenium_render_page(url)
  soup = bs(response, 'html.parser')
  results = soup.find_all(class_='product-card-container')

  # print('\nAlbertson\'s')
  for item in results[:10]:
    dict = {
      'name': item.find(class_='product-title__name').text.split(' - ')[0] 
      if '...' not in item.find(class_='product-title__name').text 
      else item.find(class_='product-item-title-tooltip__inner').text.split(' - ')[0],
      'price': float(item.find(class_='product-price__saleprice').text.split('Y')[0][1:].split('/')[0]),
      'size': item.find(class_='product-title__name').text.split(' - ')[1],
      'store': 'Albertsons'
    }
    searchResults.append(dict)


def meyer_search(query):
  baseurl = 'https://www.fredmeyer.com/'
  url= f'{baseurl}search?query={query}&searchType=default_search'
  response = selenium_render_page(url)
  print(response)
  soup = bs(response, 'html.parser')
  results = soup.find_all(class_='ProductCard')
  print(results)

  for item in results[:10]:
    dict = {
      'name': item.find(class_='kds-Text--l').text,
      'price': float(item.find(class_='kds-Price-promotional').text),
      'size': item.find(class_='kds-Text--s').text,
      'store': 'Fred Meyers'
    }
    searchResults.append(dict)


def selenium_render_page(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  sleep(3)
  r = driver.page_source
  return r

def getData(query):
  threads = []
  # threads.append(Thread(target=lambda: tj_search(query)))
  # threads.append(Thread(target=lambda: albert_search(query)))
  threads.append(Thread(target=lambda: meyer_search(query)))
  print('running...')
  for t in threads:
    t.start()

  for t in threads:
    t.join()
  # tj_search('chicken')
  # albert_search('chicken')
  sortedResults = sorted(searchResults, key=lambda i:i['price'])
  print('done!')
  return sortedResults