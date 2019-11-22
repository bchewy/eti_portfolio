import os
# Set up envrionment variables in case it cannot be found!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_portfolio.settings")

import django
django.setup()
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pytest
from django.test import Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import time
import datetime
from projects.apps import ProjectsConfig
from blog.apps import BlogConfig
from blog.models import Category, Post, Comment
from projects.models import Project


# Load the webdriver for safari and the client for django.tests.
driver = webdriver.Safari()
fake_client = Client()

# DJANGO Blog index route test
@pytest.mark.django_db
def test_list_blog_posts():
    response = fake_client.get(reverse('blog_index'))
    assert response.status_code == 200

# DJANGO Project index route test
@pytest.mark.django_db
def test_list_projects():
    response = fake_client.get(reverse('project_index'))
    assert response.status_code == 200

# DJANGO Blog Category routes test valid
@pytest.mark.django_db
def test_list_blog_category_valid():
    response = fake_client.get(
        reverse('blog_category', kwargs={'category': 'Sample'}),)
    assert response.status_code == 200

# DJANGO Blog Category routes test - invalid (opens a new page as the application's functionality is as such)
@pytest.mark.django_db
def test_list_blog_category_invalid():
    response = fake_client.get(
        reverse('blog_category', kwargs={'category': 'Acategorythatdoesnotexist'}),)
    assert response.status_code == 200

# DJANGO Blog Details routes test - valid
@pytest.mark.django_db
def test_show_blog_details_valid():
    post = create_post()
    cat = create_cat()
    comment = create_comment()
    post.categories.add(cat)
    comment.post = post
    post.save()
    response = fake_client.get(
        reverse('blog_detail', kwargs={'pk': post.id}))
    assert response.status_code == 200

# DJANGO Blog Details routes test - invalid
@pytest.mark.django_db
def test_show_blog_details_invalid():
    with pytest.raises(ObjectDoesNotExist):
        fake_client.get(
            reverse('blog_detail', kwargs={'pk': 500}))

# DJANGO Projects Details routes test - valid
@pytest.mark.django_db
def test_show_projectdetails_valid():
    project = create_project()
    response = fake_client.get(
        reverse('project_detail', kwargs={'pk': project.id}))
    assert response.status_code == 200

# DJANGO Projects 
@pytest.mark.django_db
def test_show_projectdetails_invalid():
    with pytest.raises(ObjectDoesNotExist):
        fake_client.get(
            reverse('project_detail', kwargs={'pk': 500}))


# DJANGO Comments - creating comments valid
@pytest.mark.django_db
def test_create_comments_valid():
    post = create_post()
    comment = create_comment()
    comment.post = post
    post.comments = comment
    post.save()
    response = fake_client.post(reverse('blog_detail', kwargs={'pk': post.id, }), {
                                'author': comment.author, 'body': comment.body, 'post': comment.post})
    assert response.status_code == 200

# DJANGO Comments - creating comments invalid - but still passes as empty comments go through 
# Frontend checks (to prevent the comments from being empty)
@pytest.mark.django_db
def test_create_comments_invalid():
    post = create_post()
    comment = create_comment_invalid()
    comment.post = post
    post.comments = comment
    post.save()
    response = fake_client.post(reverse('blog_detail', kwargs={'pk': post.id, }), {
                                'author': comment.author, 'body': comment.body, 'post': comment.post})
    assert response.status_code == 200

# DJANGO Check if sub-project of name projects exist
def test_project_apps_dot_py():
    assert ProjectsConfig.name == 'projects'

# DJANGO Check if sub-project of name blog exist
def test_project_blogs_dot_py():
    assert BlogConfig.name == 'blog'

# SELENIUM Check on frontend if admin page can be found
def test_initial_admin_visit():
    driver.get('http://127.0.0.1:8000/admin')
    assert "Log in | Django site admin" in driver.title

# SELENIUM CHeck the admin login works with valid username and password
def test_login_valid():
    reset_driver()
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

# SELENIUM Check if the cateogry can be created with invalid values.
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

# SELENIUM Check if the cateogry can be created with valid values.
def test_create_category_valid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)
    field = driver.find_element_by_name('name')
    field.clear()
    field.send_keys("test1")
    save_button = driver.find_element_by_xpath(
        '//*[@id="category_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="container"]/ul/li') == True and "was added successfully." in driver.page_source)

# SELENIUM Check if the category created can be viewed.
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

# SELENIUM Check if the category can be updated with valid parameters
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

# SELENIUM Check if the category can be updated with invalid parameters
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

# SELENIUM Check if the category can be deleted.
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

# SELENIUM Check if the post can be created wit invalid parameters
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

# SELENIUM Check if the post can be created wit valid parameters
def test_create_post_valid():
    driver.get('http://127.0.0.1:8000/admin')
    add_link = driver.find_element_by_xpath(
        '//*[@id="content-main"]/div[2]/table/tbody/tr[2]/td[1]/a')
    add_link.send_keys(Keys.RETURN)
    time.sleep(1)
    title = driver.find_element_by_name('title')
    title.clear()
    title.send_keys("sample title")
    body = driver.find_element_by_name('body')
    body.clear()
    body.send_keys("this is some body")
    select = Select(driver.find_element_by_xpath('//*[@id="id_categories"]'))
    select.select_by_index(1)
    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert (check_exists_by_xpath(
        '//*[@id="container"]/ul/li') == True and "was added successfully." in driver.page_source)

# SELENIUM Check if the created post can be read
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

# SELENIUM Check if the created post can be updated with valid parameters
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
    select.select_by_index(0)
    save_button = driver.find_element_by_xpath(
        '//*[@id="post_form"]/div/div/input[1]')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    assert(check_exists_by_xpath('//*[@id="container"]/ul/li') ==
           True and "was changed successfully." in driver.page_source)

# SELENIUM Check if the created post can be upadted invalid parameters
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

# SELENIUM Check if the created post can be deleted.
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

# SELENIUM Check if the user can be logged out properly after performing action.
def test_logout():
    driver.get('http://127.0.0.1:8000/admin')
    link = driver.find_element_by_xpath('//*[@id="user-tools"]/a[3]')
    link.send_keys(Keys.RETURN)
    time.sleep(1)
    assert ("Logged out | Django site admin" in driver.page_source and check_exists_by_xpath(
        '//*[@id="content"]/h1') == True)

# SELENIUM Check if the user can be logged in with invalid parameters
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
    assert check_exists_by_xpath('/html/body/div/div[2]/p') == True

# SELENIUM Check if the element cannot be found. 
def test_cannot_find_element():
    assert check_exists_by_xpath('') == False


# Common Functions
# Resets the driver and allows for the login function to be used again.
def reset_driver():
    driver.delete_all_cookies()

# Check if an element exists by the xpath - Returns true if found, false if not.
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Creates a project and save it.
def create_project():
    project = Project(title='Project Coolio',
                      description='A super cool project',
                      technology='RoR',
                      image='project1.png'
                      )
    project.save()
    return project

# Create a blog post and save it.
def create_post():
    post = Post(title='title',
                body='sample body',
                created_on=datetime.datetime.now(),
                last_modified=datetime.datetime.now())
    post.save()
    return post

# Create a category and save it.
def create_cat():
    cat = Category(name='Category')
    cat.save()
    return cat

# Create a comment and save it.
def create_comment():
    comment = Comment(author='Person',
                      body='This post rocks!',
                      created_on=datetime.datetime.now())
    return comment

# Create a invalid comment and save it.
def create_comment_invalid():
    comment = Comment(author='',
                      body='',
                      created_on=datetime.datetime.now())
    return comment
