from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

EMAIL = "******@gmail.com"
PASSWORD = "*********"

PATH = r"chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/")

#login
time.sleep(5)
username = driver.find_element_by_xpath("//input[@id='session_key']")
password = driver.find_element_by_xpath("//input[@id='session_password']")
username.clear()
password.clear()
# 														((((Login Info accounts))))
username.send_keys(EMAIL)
password.send_keys(PASSWORD)
# click login
driver.find_element_by_xpath("//button[@class='sign-in-form__submit-button']").click()
time.sleep(40)
# 														((((all accounts))))
list_account = pd.read_csv('list1.csv')['LinkedIn Profile']
time.sleep(7)

for acc in list_account:
	if acc is not EMAIL:
		driver.get(acc)
		time.sleep(5)

	# send connect if not make before
	try:
		driver.find_element_by_xpath("//div[@class='pvs-profile-actions ']/button[contains(@class,'artdeco-button artdeco-button--2')]").click()
		time.sleep(2)
		driver.find_element_by_xpath("//div[@class='artdeco-modal__actionbar ember-view text-align-right']/button[contains(@class,'artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1')]").click()
		time.sleep(2)
		print('Send request..')
	except:
		print('Already friends..')
		pass
	
	# open skills section
	try:
		skills_section = driver.find_element_by_xpath("//*[contains(span[@class='pvs-navigation__text'], 'skills')]")
		skills_section.click()
		time.sleep(3)
	except:
		continue

	# explore all skills:.
	html = driver.find_element_by_tag_name('html')
	html.send_keys(Keys.END)
	time.sleep(5)
	html.send_keys(Keys.HOME)
	time.sleep(3)
	
	# make_endorse(driver)
	endorse_list = driver.find_elements_by_xpath("//section[1]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li/div[1]/div[2]/div[2]/ul[1]/li/div[1]/button[1]")

	skills_count = len(endorse_list)
	print(f"count of element={skills_count}")
	list_of_ids = []
	for element in endorse_list:
		element_id = element.get_attribute('id')
		list_of_ids.append(element_id)

	# Make endorse
	for i in range(skills_count):
		q = f"""//div[@class='pvs-list__outer-container']/ul[@class='pvs-list
        
        ']/li[@class=' ']/div[@class='pv2']/button[@id='{list_of_ids[i]}']"""
		
		endorse = driver.find_element_by_xpath(q)
		if endorse.text == "Endorse": #and endorse.is_displayed() and endorse.is_enabled():
			print(f"[+] Do {endorse.text}")

							# ((((((((U can able to change time according to internet speed))))))))
			# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, q))).click()
			driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, q))))
			# 	ActionChains(driver).move_to_element(endorse).click().perform()
			time.sleep(10)

			# ignore show more skills button
			if driver.find_elements_by_xpath("//div[@class='display-flex p5']").__len__():
				# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='display-flex p5']/button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']/span[@class='artdeco-button__text']"))).click()
				ActionChains(driver).move_to_element(driver.find_element_by_xpath("//div[@class='display-flex p5']/button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']/span[@class='artdeco-button__text']")).click().perform()

			time.sleep(3)
			endorse_list = driver.find_elements_by_xpath("//section[1]/div[2]/div[2]/div[1]/div[1]/div[1]/ul[1]/li/div[1]/div[2]/div[2]/ul[1]/li/div[1]/button[1]")

			list_of_ids = []
			for element in endorse_list:
				element_id = element.get_attribute('id')
				list_of_ids.append(element_id)
			print(f"No. [{i+1}], from total [{len(list_of_ids)}]")

		else:
			print(f'[-] Already {endorse.text}')


	
	print("****"*30)
	print(f"Successfully Endorse {acc} 🦾✨")
	print("****"*30)

print("====="*20)
print(f"Done, Finish Endorse all accounts 😍")
print("====="*20)
driver.close()

print("====== ⚠🛑 Don't Forget remove Email and Password from file after finish‼ 🛑⚠ ========")