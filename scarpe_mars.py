from bs4 import BeautifulSoup as _soup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import urllib.request,sys,time

def scrape_all():

	#NASA Mars News - Step 1
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)

	nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
	browser.visit(nasa_url)

	browser.is_element_present_by_css('li.slide',wait_time=1)

	html=browser.html

	soup=_soup(html,'html.parser')

	results = soup.select_one('ul.item_list li.slide')
	title=results.find('div', class_='content_title').get_text()

	paragraph=results.find('div', class_='article_teaser_body').get_text()
	
	#JPL Mars Space Images - Step 1

	mars_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
	browser.visit(mars_url)
	time.sleep(1)

	browser.find_by_css('img.BaseImage').click()
	time.sleep(3)

	html = browser.html
	soup = _soup(browser.html, 'html.parser')

	featured_image_url= soup.find('a', class_='BaseButton')['href']

	#Mars Facts - Step 1

	facts_url = 'https://space-facts.com/mars/'

	tables = pd.read_html(facts_url)

	df = tables[0]
	# df.columns=['description', 'mars']
	df.set_index('description',inplace=True)

	mars_table=df.to_html()

	#Mars Hemispheres - Step 1

	hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemispheres_url)

	link_list=browser.find_by_css('a.product-item h3')

	list_planets=[]

	for i in range(len(link_list)):
		planets={}

		browser.find_by_css('a.product-item h3')[i].click()
		planets['picture'] = browser.links.find_by_text('Sample').first['href']
		planets['title']=browser.find_by_css('h2.title').text
		list_planets.append(planets)

		browser.back()
    
	
	step1_dic={
			'title': title,
			'paragraph': paragraph,
			'feature_image': featured_image_url,
			'mars_table': mars_table,
			'planets': list_planets}

	return step1_dic


