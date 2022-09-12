#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:01:28 2021

@author: xiaowenfeng
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
#新增資料夾
os.makedirs('./file_txt')
a = os.getcwd() #存原本路徑

#get funday
driver = webdriver.Chrome('./chromedriver')  
driver.get('https://tts-nptu.funday.asia/');

#登入
def login_(a_p):
    account = driver.find_element(By.NAME, 'email')
    accstr = a_p #input('account: ')
    account.send_keys(accstr)
    passwd = driver.find_element(By.NAME, 'password')
    passstr = a_p #input('passwd: ')
    passwd.send_keys(passstr)
    passwd.submit()

def click_(name):
    #Click
    lttc='https://tts-nptu.funday.asia/default/Lttc.asp'
    driver.get(lttc)
    time.sleep(2)
    xpath_ = f"//*[text()='{name}']"    
    try:
        driver.find_element(By.XPATH, xpath_).click()
    except:
        element = driver.find_element_by_xpath(xpath_)
        driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    #定位iframe Click
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="newsdiv"]/iframe'))
    driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div[5]/iframe'))
    driver.find_element(By.XPATH, '//*[@id="content"]/table[1]/tbody/tr[5]/td/a/img').click()
    time.sleep(2)
    driver.switch_to.parent_frame()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="divIframe"]'))
    time.sleep(2)
    #切換到資料夾
    os.chdir('./file_txt')
    #爬取文字
    filename = f"{name}.txt"
    addfile(filename)
    #退出iframe
    #driver.switch_to.default_content()
    #回到原本路徑
    os.chdir(a)
    
def addfile(filename):
    soup = BeautifulSoup(driver.page_source)
    with open(filename , "w", encoding='UTF-8')as f:
        for s in soup.find_all('div', {'class': 'FontSpace'}):
            print(s.text)    
            f.write(s.text) 
            f.write("\n")
    
name = ["健身房","U-bikes 騎車趣","下雨天","蛋炒飯","在家看DVD","課堂小考","周末計畫","外出用餐" \
        ,"找提款機","看醫生","百貨公司購物","喝杯咖啡","搭計程車","自助加油","租套房","買鞋趣"]

login_("CBF108008")
for n in name:
    click_(n)
    time.sleep(2)

    
driver.close()