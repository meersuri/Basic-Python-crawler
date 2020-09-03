from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
import time

#use Google Chrome as the webdriver
driver = webdriver.Chrome()
# driver.implicitly_wait(10) # seconds
#e-commerce website url
url = "https://shopee.tw/%E7%8E%A9%E5%85%B7-cat.75.2185?brands=5005&locations=-1&page=0&ratingFilter=4"
#load webpage using the webdriver and wait to allow full loading
driver.get(url)
#need a better way to wait for page loading and scrolling to get all the data fromt the page
time.sleep(5)
height = 0
scroll_height = driver.execute_script("return document.body.scrollHeight")
while height < scroll_height:
	driver.execute_script("window.scrollBy(0, 300);")
	height += 300
	time.sleep(2)
#get HTML source code from the loaded page
page_source = driver.page_source
#parse using BeautifulSoup's html parser
soup = BeautifulSoup(page_source, 'html.parser')
	
all_titles = []
all_prices = []
#get product titles based on their HTML code which can be viewd by using inspect element in Chrome
for div in soup.find_all('div', attrs={'class':'_3eufr2'}):
    title = div.find('div', attrs={'class':'_1NoI8_ _16BAGk'})
	#title can be None sometimes
    if title:
        all_titles.append(title.text)
	#some items have price ranges so use find_all
    price = div.find_all('span', attrs={'class':'_341bF0'})
    if price:
        all_prices.append([p.text for p in price])
		
#load conversion table
converter = {}
with open('./traditional_to_simplified_table.pkl', 'rb') as fp:
    converter = pickle.load(fp)

#convert traditional to simplified
all_simplified_titles = []
for title in all_titles:
    simplified_title = ''.join([converter[c] if c in converter else c for c in title])
    all_simplified_titles.append(simplified_title)

#output simplified titles concatenated with prices
output = []
for title, price in zip(all_simplified_titles, all_prices):
	#for a single price
    if len(price) == 1:
        output.append(title + ' $' + price[0])
	#for price range
    elif len(price) == 2:
        output.append(title + ' $' + price[0] + '-' + '$' + price[1])

#write output to txt file
with open('simplified_output.txt', 'w', encoding="utf-8") as f:
    f.write('\n'.join(output))

driver.quit()