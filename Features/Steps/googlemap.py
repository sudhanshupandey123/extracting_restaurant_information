from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

paths = {
    'search_box_xpath': "//input[@id='searchboxinput']",
    'searched_interest_list_xpath': "//*[@class='Nv2PK THOPZb CpccDe ']/child::a",
    'restaurant_name_xpath': "//h1[@class='DUwDvf lfPIob']",
    'restaurant_rating_xpath': "//span[@class='ceNzKf']/preceding-sibling::span",
    'restaurants_address_xpath': "(//div[@class='rogA2c ']/child::div)[1]",
    'restaurant_review_xpath': "(//div[@class='F7nice ']/child::span)[2]",
  
}


@given(u'He Open Google Map')
def opening_google_map(context):
    """
    Opening Google Map
    """
    context.driver = webdriver.Chrome()
    context.driver.get('https://www.google.com/maps/')
    context.driver.maximize_window()
    '''Creating A Empty List To Store ALL Details Of Searched Things '''
    context.details = []


@when(u'He Search For "{user_searched_for}"')
def search_your_interest(context, user_searched_for):
    """ Searching Things On Map
    'user_searched_for: Store the details what user searched in map in string format
    """
    context.interest = user_searched_for
    context.driver.find_element(By.XPATH, paths['search_box_xpath']).send_keys(user_searched_for, Keys.ENTER)
    context.driver.implicitly_wait(10)


@when(u'He Found The List')
def checking_list_found_or_not(context):
    """
     If List After searching element found it will not throw exception otherwise it will throw error
     Just To Check Whether Map is able to give result based on user input or not
    """
    wait = WebDriverWait(context.driver, 10)
    context.all_link = wait.until(
        ec.presence_of_all_elements_located((By.XPATH, paths['searched_interest_list_xpath'])))
    try:
        assert context.all_link != [], 'Unable To Find Required List'
    except AssertionError as msg:
        print(msg)


@when('He Save Top "{user_requirement_value}" All The Details')
def extracting_details(context, user_requirement_value):
    """
    :param user_requirement_value: Stores Total Number of Interest User Want To Save Details
    :return: It Returns CSV File Of Searched Item
    """
    X = []
    tot = []
    list_of_searched_interest = context.driver.find_element(By.XPATH, paths['searched_interest_list_xpath'])

    def extracting_information(list_of_searched_result):
        for i in range(len(list_of_searched_result)):
            if len(context.details) > int(user_requirement_value):
                break
            if tot[i] not in X:
                D = {}
                time.sleep(2)
                tot[i].click()
                time.sleep(5)

                try:
                    D['name'] = context.driver.find_element(By.XPATH, paths['restaurant_name_xpath']).text
                except:
                    D['name'] = 'NULL'

                try:
                    D['rating'] = context.driver.find_element(By.XPATH,
                                                              paths['restaurant_rating_xpath']).text
                except:
                    D['rating'] = 'NULL'

                try:
                    D['address'] = context.driver.find_element(By.XPATH, paths['restaurants_address_xpath']).text
                except:
                    D['address'] = 'NULL'

                try:
                    D['review'] = context.driver.find_element(By.XPATH, paths['restaurant_review_xpath']).text
                except:
                    D['review'] = 'NULL'
                try:
                    url = str(context.driver.current_url)
                    filtering_lat_and_long = re.search('@\d+\S{1}\d+,\d+\S{1}\d+', url)
                    D['Log_and_Lat'] = filtering_lat_and_long.group()
                    D['Log_and_Lat'] = D['Log_and_Lat'].replace('@', '')
                except:
                    D['Log_and_Lat'] = 'NULL'
            X.append(tot[i])
            context.details.append(D)
            list_of_searched_interest.send_keys(Keys.DOWN)

    while True:
        if len(tot) >= int(user_requirement_value):
            break
        else:
            tot = context.driver.find_elements(By.XPATH, "//*[@class='Nv2PK THOPZb CpccDe ']/child::a")
            list_of_searched_interest.send_keys(Keys.END)
    extracting_information(set(tot))


@then('He Make CSV File Of Those')
def making_csv(context):
    """
    Finally Making CSV Files Of the Informations
    :param context:
    :return:
    """
    empty_d = []
    if context.interest not in empty_d:
        empty_d.append(context.interest)
        field_names = ['name', 'rating', 'address', 'review', 'Log_and_Lat']
        with open(f'{context.interest}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(context.details)
    empty_d.append(context.interest)
    context.driver.quit()
