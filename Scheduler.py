import requests
import selenium
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import smtplib
import os
from twilio.rest import Client
import datetime
import Send
import Cred

DATA_STRUCTURES_UOCLINK = "https://sis.rutgers.edu/soc/#keyword?keyword=DATA%20STRUCTURES&semester=12023&campus=NB&level=U"

def openUOC(driver) :
    driver.get(DATA_STRUCTURES_UOCLINK)    
    element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.highlighttext"))
        )

def expandCourses(driver):
    driver.find_element_by_id("subjectTitle2").click()
    
def parseMetaData(driver, profName):
    sections = driver.find_elements_by_css_selector('div.sectionListings div.section div.sectionData')
    for section in sections:
        try:               
            if(str(profName) in section.text):
                if(len(section.find_elements_by_css_selector('span.sectionclosed')) == 0):
                    print("CLASS AVAILABLE\n")
                    print(section.text)
                    Send.send('CLASS IS AVAILABLE!!!')
                    Send.send(str(section.text[2:7]))
                    sectionLink = f'https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&amp;semesterSelection=12023&amp;indexList={section.text[2:7]}'
                    Send.send(str(sectionLink))
                    return autoRegister(driver, str(sectionLink))
            else:
                print("NO CLASS")
                print(section.text[2:7], "\n")
        except:
            print("error")

def printTime():
    x = datetime.datetime.now()
    print(f"----------------------------\n{x.strftime('%X')}\n----------------------------")
    
def closeDriver(driver):
    driver.close()

def autoRegister(driver, link):
    driver.get(link)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password")))
    driver.find_element_by_css_selector("input#username").send_keys(str(Cred.username))
    driver.find_element_by_css_selector("input#password").send_keys(str(Cred.password))
    driver.find_element_by_css_selector('input.btn').click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#duo_iframe")))
    frame = driver.find_element_by_css_selector('iframe#duo_iframe')
    driver.switch_to.frame(frame)
    driver.find_elements_by_css_selector('button.positive')[0].click()
    isOnAuthScreen = True
    Counter = 0;
    while (isOnAuthScreen and Counter < 5):
        try:
            if(driver.find_element_by_css_selector('span.message-text').text == "Login timed out."):
                driver.find_elements_by_css_selector('button.positive')[0].click()            
        except:
            print('LOGIN WINDOW ACTIVE')
        try:
            if(driver.find_element_by_css_selector('input#submit')):
                isOnAuthScreen = False
        except:
            print('STILL ON AUTH SCREEN')
        time.sleep(10)
        Counter = Counter + 1
    
    if(not (Counter >= 5)):
        driver.find_element_by_css_selector('input#submit').click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#i1")))
        driver.find_element_by_css_selector('input#i1').send_keys(str(link[101:]))
        driver.find_element_by_css_selector('input#submit').click()
        time.sleep(1)
        Send.send('COURSE ADDED')
        return True        
    else:
        return False
def check():
    driver = webdriver.Chrome("C:\\Users\\tejas_6\\OneDrive\\Desktop\\Chorme\\chromedriver.exe")
    openUOC(driver)
    expandCourses(driver)
    bool = parseMetaData(driver, "CENTENO")
    printTime()
    closeDriver(driver)
    if(bool):
        return True
    else:
        return False    
    

    
if __name__ == "__main__":
    # delete this after testing
    #driver = webdriver.Chrome("C:\\Users\\tejas_6\\OneDrive\\Desktop\\Chorme\\chromedriver.exe")
    #autoRegister(driver, "https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&amp;semesterSelection=12023&amp;indexList=04562")
    while(True):
        try:
            isCourseAdded = check()
            if(isCourseAdded):
                break
            time.sleep(3)
        except Exception as e:
            Send.send('Error With Code')
            Send.send(str(e))
    Send.send('Terminated Program, goodbye')
