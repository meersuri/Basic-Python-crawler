from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pickle
import time

def has_chinese(text):
    """ checks if given text contains any chinese characters """
    if re.search('[\u4e00-\u9fff]', text):
        return True
    return False
#use Google Chrome as the webdriver
driver = webdriver.Chrome()
#traditional to simplified conversion table url
table_url = "https://phabricator.wikimedia.org/source/mediawiki/browse/master/languages/data/ZhConversion.php"
#load webpage using the webdriver
driver.get(table_url)
#need a better way to wait for page loading
time.sleep(5)
#get HTML source code from the loaded page
page_source = driver.page_source
#parse using BeautifulSoup's html parser
soup = BeautifulSoup(page_source, 'html.parser')

#dictionary to map traditional to simplified
converter = {}
#some chars are repeated, need further investigation to see if they have different mappings to simplified chars
repeats = []
all_source_code = []
for i, tr in enumerate(soup.find_all("tr")):
	#scrape only lines of source code
    source_code = tr.find('td', attrs = {'class':'phabricator-source-code'})
    source_code = source_code.text
    all_source_code.append(source_code)
	#we only need lines of source code that map from traditional to simplified
    if has_chinese(source_code):
        chars = source_code.strip(',\n').split(' ')
        traditional = chars[0][1:-1]
        simplified = chars[2][1:-1]
        if traditional not in converter:
            converter[traditional] = simplified
        else:
            repeats.append(traditional)
			
driver.close()

#write conversion table to disk
with open('./traditional_to_simplified_table.pkl', 'wb') as fp:
    pickle.dump(converter, fp)