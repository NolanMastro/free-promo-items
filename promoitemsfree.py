import os
import traceback
import requests
import datetime
import random
import string
import discord
import names
from discord import SyncWebhook
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


url = 'discord webhook url to send the account info.'
catchall = 'your catchall, example @hello.xyz'
password = 'the password you want to use for the accounts'
colors = ['Trans Green', 'Black', 'Trans Orange', 'Purple', 'Trans Red', 'Trans Blue', 'White', 'Silver']
address = ' your address here (KEEP A SPACE BEFORE IT)'
zip_code = 'your zip code here'
item_names = ['Syringe Highlighter/Pen', '3/4" Stretchy Elastic Dye Sublimation Wristbands', 'Wooden Cube Grow Kit', 'Small Chalkboard Magnet 7 x 8-1/4', 'Puzzle/Maze Pen', 'Bamboo 22 oz Frosted Glass Bottle']
area_code = '408'



def main():
    options = webdriver.ChromeOptions()
    driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=30).install()),options=options)
    driver.get('https://www.anypromo.com/CustomerLogin.aspx?returnurl=%2fGetASample_Succeed.aspx%3fSampleID%3dSM1848873 ')
    while True:
        create_account(driver, catchall, password, address, zip_code, url, item_names, area_code)



def create_account(driver, catchall, password, address, zip_code, url, item_names, area_code):
    #create account button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-body-l > div.div-login > div.div-login-new'))).click()
    #names
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-body-r > div.div-input > table > tbody > tr:nth-child(1) > td:nth-child(1) > input'))).send_keys(names.get_first_name())
    driver.find_element(By.CSS_SELECTOR, '#main-body-r > div.div-input > table > tbody > tr:nth-child(1) > td:nth-child(2) > input').send_keys(names.get_last_name())
    #industry dropdown
    elem = driver.find_element(By.CSS_SELECTOR, '#ddlIndustry')
    elem.click()
    elem = Select(elem)
    elem.select_by_index(random.randint(1,10))
    #position dropdown
    elem = driver.find_element(By.CSS_SELECTOR, '#ddlDepartment')
    elem.click()
    elem = Select(elem)
    elem.select_by_index(random.randint(1,8))
    #email/pass
    random_email = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    random_email = random_email + catchall
    driver.find_element(By.CSS_SELECTOR, '#main-body-r > div.div-input > table > tbody > tr:nth-child(5) > td > input').send_keys(random_email)
    driver.find_element(By.CSS_SELECTOR, '#main-body-r > div.div-input > table > tbody > tr:nth-child(6) > td > input.input-1.hideShowPassword-field').send_keys(password)
    #phone
    random_number = ''.join(random.choice(string.digits) for _ in range(10))
    random_number = area_code + random_number
    driver.find_element(By.CSS_SELECTOR, '#text_phone').send_keys(random_number)
    #uncheck box about emails
    driver.find_element(By.CSS_SELECTOR, '#main-body-r > div.div-login > div:nth-child(2) > label > i').click()
    #create account button
    driver.find_element(By.CSS_SELECTOR, '#main-body-r > div.div-login > div.div-register-button.register-btn-blue').click()
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ucHeader_txtSearch')))
    #buy item
    elem = driver.find_element(By.CSS_SELECTOR, '#ucHeader_txtSearch')
    item = random.choice(item_names)
    elem.send_keys(item)
    elem.send_keys(Keys.ENTER)
    #get item
    driver.find_element(By.CSS_SELECTOR, '#onsale_item0 > div > div.onsale_name > a').click()
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-price > div.main-right.row > div.main-total > div.total-table.row.no-border > div.total-border.total-normal > ul.price-buttons.total-inner.ptnew > li.show.order-buttons > div > a.btn.sample-btn'))).click()
    
    #shipping info
    sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR, '#step1_continue').click()
    except:
        pass
    sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#a_text_firstname'))).send_keys(names.get_first_name())
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#a_text_lastname').send_keys(names.get_last_name())
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#a_text_phone').send_keys(random_number)
    sleep(1)
    jig = ''.join(random.choice(string.ascii_letters) for _ in range(3))
    jig = jig.lower()
    driver.find_element(By.CSS_SELECTOR, '#a_text_address').send_keys(jig + address)
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#zipcode_zipCodeTD1').send_keys(zip_code)
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#stepAddress_continue').click()
    WebDriverWait(driver, 109).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rdAddressVerification_0'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#continueSuggest'))).click()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#stepMethod_continue'))).click()
    except:
        pass
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_placeyouorder2'))).click()
    #send info to discord
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#main > div > div.Confirmation-left > div.order-number > a')))
    order_number = driver.find_element(By.CSS_SELECTOR, '#main > div > div.Confirmation-left > div.order-number > a').text.strip()
    embed=discord.Embed(title="Success!", color=0x5b0085)
    embed.add_field(name="Email: ", value=random_email, inline=False)
    embed.add_field(name="Password: ", value=password, inline=False)
    embed.add_field(name="Item Name: ", value=item, inline=False)
    embed.add_field(name="Order Number: ", value=order_number, inline=False)
    embed.set_footer(text="by nono#0618")
    webhook = SyncWebhook.from_url(url)
    webhook.send(embed=embed)
    #sign out
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#head-loginin')))
    elem = driver.find_element(By.CSS_SELECTOR, '#head-loginin')
    logout_button = driver.find_element(By.CSS_SELECTOR, '#adminLoginHeight > ul > li:nth-child(3) > a')
    Hover = ActionChains(driver).move_to_element(elem).move_to_element(logout_button)
    Hover.click().perform()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#head-loginin > a'))).click()

    


main()