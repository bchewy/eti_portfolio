from selenium.common.exceptions import NoSuchElementException
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

driver = webdriver.Safari()


# Checks if the initial visit to the /admin route works
def test_initial_visit():
    driver.get('http://127.0.0.1:8000/projects')
    assert check_exists_by_xpath('/html/body/nav/div/a') == True


def test_check_resume():
    driver.get('http://127.0.0.1:8000/projects')
    time.sleep(5)
    resume = driver.find_element_by_name("myresume")
    assert "My Resume" in resume.text


# Common Functions
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
