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
details=[]
@given(u'He Open Google Map')
def opening_google_map(context):
    """
    Opening Google Map
    """
    context.driver=webdriver.Chrome()
    context.driver.get('https://www.google.com/maps/')
    context.driver.maximize_window()

@when(u'He Search For "{search_input}"')
def search_your_interest(context,search_input):
    """ Searching Things On Map
    """
    context.interest=search_input
    context.driver.find_element(By.XPATH,"//input[@id='searchboxinput']").send_keys(search_input,Keys.ENTER)
    time.sleep(5)


@when(u'He Found The List')
def checking_list_found(context):
    """
     If List After searching element found it will not throw any exception otherwise it will throw error
    """
    wait=WebDriverWait(context.driver,10)
    context.all_link = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//*[@class='Nv2PK THOPZb CpccDe ']/child::a")))
    assert context.all_link != [], 'Unable To Find Required List'


@when('He Save Top "{total_count}" All The Details')
def saving_details(context,total_count):
    """
    :param total_count: Storing Total Number Of Interest For Saving Details
    :return: It Returns CSV File Of Searched Item
    """
    X = []
    tot = []
    all_link = context.driver.find_element(By.XPATH, "//*[@class='Nv2PK THOPZb CpccDe ']/child::a")
    def extracting_information(arg):
        tot_list=set(arg)
        for i in range(len(tot_list)):
            if len(details)>int(total_count):
                break
            if tot[i] not in X:
                D = {}
                tot[i].click()
                time.sleep(5)

                try:
                    D['name'] = context.driver.find_element(By.XPATH, "//h1[@class='DUwDvf lfPIob']").text
                except:
                    D['name'] = 'NULL'

                try:
                    D['rating'] = context.driver.find_element(By.XPATH,
                                                              "//span[@class='ceNzKf']/preceding-sibling::span").text
                except:
                    D['rating'] = 'NULL'

                try:
                    D['address'] = context.driver.find_element(By.XPATH, "(//div[@class='rogA2c ']/child::div)[1]").text
                except:
                    D['address'] = 'NULL'

                try:
                    D['review'] = context.driver.find_element(By.XPATH, "(//div[@class='F7nice ']/child::span)[2]").text
                except:
                    D['review'] = 'NULL'
                try:
                    url = str(context.driver.current_url)
                    lan = re.search('@\S+,\S+,', url)
                    D['Log_and_Lat'] = lan.group()
                    D['Log_and_Lat'].replace('@', '')
                    D['Log_and_Lat'].replace(',', ' ')
                except:
                    D['Log_and_Lat'] = 'NULL'
            X.append(i)
            details.append(D)
            all_link.send_keys(Keys.DOWN)

    while True:
        if len(tot)>=int(total_count):
            break
        else:
            tot = context.driver.find_elements(By.XPATH, "//*[@class='Nv2PK THOPZb CpccDe ']/child::a")
            all_link.send_keys(Keys.END)
    extracting_information(set(tot))


@then('He Make CSV File Of Those')
def making_csv(context):
    field_names = ['name', 'rating', 'address', 'review', 'Log_and_Lat']
    with open('new_file.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(details)
    context.driver.close()








