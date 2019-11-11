from selenium.common.exceptions import NoSuchElementException
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Safari()


# Checks if the initial visit to the /admin route works
def test_initial_visit():
    driver.get('http://127.0.0.1:8000/admin')
    assert "Log in | Django site admin" in driver.title


# Checks for the initial visit to the /admin route and logs on.
def test_login_valid():
    driver.get('http://127.0.0.1:8000/admin')
    username_e = driver.find_element_by_name("username")
    password_e = driver.find_element_by_name("password")
    username_e.clear()
    password_e.clear()
    username_e.send_keys("brianchew")
    password_e.send_keys("brian123@")
    username_e.send_keys(Keys.RETURN)
    time.sleep(1)
    assert check_exists_by_xpath('//*[@id="user-tools"]') == True


def test_create_category_invalid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)
    save_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="category_form"]/div/p') == True and "Please correct the error below." in driver.page_source)


def test_create_category_valid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)
    # Fill in the category field
    field = driver.find_element_by_name('name')
    field.clear()
    field.send_keys("test1")
    save_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="container"]/ul/li') == True and "was added successfully." in driver.page_source)


def test_read_created_category():
    driver.get('http://127.0.0.1:8000/admin')
    category_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/th/a')
    category_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    assert "Change category" in driver.page_source


def test_update_created_category_valid():
    driver.get('http://127.0.0.1:8000/admin')
    category_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/th/a')
    category_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    field = driver.find_element_by_xpath('//*[@id="id_name"]')
    field.clear()
    field.send_keys("newcategory")
    save_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert(check_exists_by_xpath('//*[@id="container"]/ul/li') ==
           True and "was changed successfully." in driver.page_source)


def test_update_created_category_invalid():
    driver.get('http://127.0.0.1:8000/admin')
    category_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/th/a')
    category_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    field = driver.find_element_by_xpath('//*[@id="id_name"]')
    field.clear()
    field.send_keys("")
    save_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="category_form"]/div/p') == True and "Please correct the error below." in driver.page_source)


def test_delete_created_category():
    driver.get('http://127.0.0.1:8000/admin')
    change_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[2]/a')
    change_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    delete_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/p/a')
    delete_button.send_keys(Keys.RETURN)
    time.sleep(1)
    confirm_button = driver.find_element_by_xpath(
        '//*[@id="content"]/form/div/input[2]')
    confirm_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert(check_exists_by_xpath('//*[@id="container"]/ul/li') ==
           True and "was deleted successfully." in driver.page_source)


def test_create_post_invalid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)
    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="post_form"]/div/p') == True and "Please correct the errors below." in driver.page_source)


def test_create_post_valid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)

    # Fill in the fields
    title = driver.find_element_by_name('title')
    title.clear()
    title.send_keys("sample title")
    body = driver.find_element_by_name('body')
    body.clear()
    body.send_keys("this is some body")
    select = Select(driver.find_element_by_xpath('//*[@id="id_categories"]'))
    select.select_by_index(1)  # Select the first category to be linked

    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="container"]/ul/li') == True and "was added successfully." in driver.page_source)


def test_read_created_post():
    driver.get('http://127.0.0.1:8000/admin')
    post_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/th/a')
    post_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    assert "Change post" in driver.page_source


def test_update_created_post_valid():
    driver.get('http://127.0.0.1:8000/admin')
    post_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/th/a')
    post_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)

    title = driver.find_element_by_name('title')
    title.clear()
    title.send_keys("new sample title")
    body = driver.find_element_by_name('body')
    body.clear()
    body.send_keys("this is some new body")
    select = Select(driver.find_element_by_xpath('//*[@id="id_categories"]'))
    select.select_by_index(0)  # Select the first category to be linked

    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert(check_exists_by_xpath('//*[@id="container"]/ul/li') ==
           True and "was changed successfully." in driver.page_source)


def test_update_created_post_invalid():
    driver.get('http://127.0.0.1:8000/admin')
    post_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/th/a')
    post_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)

    title = driver.find_element_by_name('title')
    title.clear()
    title.send_keys("")
    body = driver.find_element_by_name('body')
    body.clear()
    body.send_keys("")

    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="post_form"]/div/p') == True and "Please correct the errors below." in driver.page_source)


def test_delete_created_post():
    driver.get('http://127.0.0.1:8000/admin')
    change_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/td[2]/a')
    change_link.send_keys(Keys.RETURN)
    time.sleep(1)
    first_object = driver.find_element_by_xpath(
        '//*[@id="result_list"]/tbody/tr[1]/th/a')
    first_object.send_keys(Keys.RETURN)
    time.sleep(1)
    delete_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/p/a')
    delete_button.send_keys(Keys.RETURN)
    time.sleep(1)
    confirm_button = driver.find_element_by_xpath(
        '//*[@id="content"]/form/div/input[2]')
    confirm_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert(check_exists_by_xpath('//*[@id="container"]/ul/li') ==
           True and "was deleted successfully." in driver.page_source)


def test_logout():
    driver.get('http://127.0.0.1:8000/admin')
    link = driver.find_element_by_xpath('//*[@id="user-tools"]/a[3]')
    link.send_keys(Keys.RETURN)
    time.sleep(1)
    assert ("Logged out | Django site admin" in driver.page_source and check_exists_by_xpath(
        '//*[@id="content"]/h1') == True)


def test_login_invalid():
    reset_driver()
    driver.get('http://127.0.0.1:8000/admin')
    username_e = driver.find_element_by_name("username")
    password_e = driver.find_element_by_name("password")
    username_e.clear()
    password_e.clear()
    username_e.send_keys("fakeusername")
    password_e.send_keys("wrongpassword")
    username_e.send_keys(Keys.RETURN)
    time.sleep(1)
    # Check for error note element
    assert check_exists_by_xpath('/html/body/div/div[2]/p') == True

# Common Functions


def reset_driver():
    driver.delete_all_cookies()


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
