import pdb
import sys
import csv
import time
import progressbar
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def write(dic):
	keys = dic[0].keys()
	with open('followers.csv','wb') as fp:
		dict_writer = csv.DictWriter(fp,keys)
		dict_writer.writeheader()
		dict_writer.writerows(dic)

def get_follows(source):
	soup = BeautifulSoup(source,'html.parser')
	stream = soup.find('div',class_="stream")
	ol = stream.find('ol')
	items = ol.find_all('li',class_='js-activity-follow')
	result = []
	print "Analysing followers list..."
	pb = progressbar.ProgressBar()
	for item in pb(items):
		dt = item.find('span',class_="_timestamp").text
		users = item.find('ol').find_all('li')
		for user in users:
			anchor = user.find('a')
			try:
				result.append({'date': str(dt),'u_id': str(anchor['data-user-id']),'u_name': str(anchor['title'])})
			except Exception:
				continue
	return result


def get_page_source():

	browser = ''
	action = ''

	#pdb.set_trace()
	try:
		#pdb.set_trace()
		browser = webdriver.Chrome("lib/chromedriver-"+sys.argv[1])
		action  = ActionChains(browser)
		browser.get("http://www.twitter.com")
	except Exception:
	 	print "Error occured. Check internet connectivity and try again"

	action.move_to_element(browser.find_element_by_class_name("StreamsLogin")).click().perform()
	print "Please enter your username and password in the browser...."

	try:
		notifications = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "notifications")))
	except:
		print "Error"
		browser.quit()		

	for i in range(4):
		try:
			run_test = WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "notifications")))
			run_test.click()
			break
		except Exception as e:
			raise e
	print "Collecting followers list...."
	while True:
		try:
			WebDriverWait(browser,5).until(EC.visibility_of(browser.find_element_by_class_name("stream-end")))
			break
		except Exception:
			time.sleep(5)
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			continue

	result = browser.page_source

	browser.quit()

	return result

src = get_page_source()
data = get_follows(src)
write(data)
print "Done. Please email the newly created 'followers.csv' file to anupamaa@iiitd.ac.in"