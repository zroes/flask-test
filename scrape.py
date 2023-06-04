from bs4 import BeautifulSoup as bs
from time import sleep, perf_counter
# from requests_html import AsyncHTMLSession, HTMLSession
# import asyncio
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

searchResults = []

def tj_search(query):
  baseurl = 'https://www.traderjoes.com/'
  url = f'{baseurl}home/search?q={query}&section=products&global=yes'
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
  url = f'{baseurl}shop/search-results.html?q={query}'
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
  # print(response)
  soup = bs(response, 'html.parser')
  results = soup.find_all(class_='ProductCard')
  # print(results)

  for item in results[:10]:
    dict = {
      'name': item.find(class_='kds-Text--l').text,
      'price': float(item.find(class_='kds-Price-promotional').text[1:]),
      'size': item.find(class_='text-neutral-more-prominent').text,
      'store': 'Fred Meyer'
    }
    searchResults.append(dict)


def wf_search(query):
  baseurl = 'https://www.wholefoodsmarket.com/'
  url = f'{baseurl}search?text={query}'
  response = selenium_render_page(url, True)
  # print(response)
  soup = bs(response, 'html.parser')
  results = soup.find_all(class_='w-pie--product-tile')

  for item in results[:10]:
    dict = {
      'name': 
        item.find(class_='w-cms--font-disclaimer').text + 
        ' ' + 
        item.find(class_='w-cms--font-body__sans-bold').text.split(',')[0],
      'price': float(item.find(class_='sale_price').text[11:]) 
        if item.find(class_='sale_price') 
        else float(item.find(class_='regular_price').text[1:]),
      'size': item.find(class_='w-cms--font-body__sans-bold').text.split(', ')[1] 
        if len(item.find(class_='w-cms--font-body__sans-bold').text.split(', ')) > 1 
        else 'null',
      'store': 'Whole Foods'
    }
    searchResults.append(dict)


def selenium_render_page(url, from_wf=False):
  # chrome_options = Options()
  # chrome_options.add_argument('--headless')
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
  options = webdriver.ChromeOptions() 

  options.add_argument('--headless')
  options.add_argument(f'user-agent={user_agent}')
  driver = webdriver.Chrome(
    # executable_path='chromedriver_mac_arm64/chromedriver', 
    options=options
  )
  driver.get(url)
  if from_wf:
    print('from whole foods')
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 43.6110909,
            "longitude": -116.3032469,
            "accuracy": 100
    })
    sleep(2)
    modal = driver.find_element(By.CLASS_NAME, 'modal--content')
    modal.find_element(By.CLASS_NAME, 'w-makethismystore').click()
    sleep(0.1)
    driver.switch_to.alert.dismiss();
  sleep(3)
  r = driver.page_source
  return r


def getData(query):
  threads = []
  global searchResults
  searchResults = []
  # query = query.replace(' ', '%20')
  print(query)
  threads.append(Thread(target=lambda: tj_search(query)))
  threads.append(Thread(target=lambda: albert_search(query)))
  threads.append(Thread(target=lambda: meyer_search(query)))
  threads.append(Thread(target=lambda: wf_search(query)))
  print('running...')
  for t in threads:
    t.start()

  for t in threads:
    t.join()
  # tj_search('chicken')
  # albert_search('chicken')
  sortedResults = sorted(searchResults, key=lambda i:i['price'])
  print('done!')
  return searchResults