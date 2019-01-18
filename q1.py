import os
import random
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from operator import itemgetter
from explicit import waiter, XPATH
from selenium.common.exceptions import NoSuchElementException
import string
import re
from nltk.corpus import stopwords
import xlsxwriter
import math

data = {
    "username" : "",
    "password" : "",
    "url" : ""
}
def findNumberOfFollowersAndFollowing(driver):
    #find number of followers
    followersAmount = driver.find_element_by_xpath("//li[2]/a/span").text
    followersAmount = followersAmount.replace(',', "")

    if 'k' in followersAmount:
        followersAmount = followersAmount[:-1]
        followersAmount = int(float(followersAmount)) * 1000

    else:
        followersAmount = int(float(followersAmount))


    #find number of following
    followingAmount = (driver.find_element_by_xpath("//li[3]/a/span").text).replace(',',"")
    if 'k' in followingAmount:
        followingAmount = followingAmount[:-1]
        followingAmount = int(float(followingAmount)) * 1000

    else:
        followingAmount = int(float(followingAmount))

    return followersAmount, followingAmount

def isMutual(account1, account2,driver):
    data["url"] = 'https://www.instagram.com/' + account1 + '/followers/'
    driver.get(data["url"])
    driver.maximize_window()

    WebDriverWait(driver, 20).until(
        EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + account1 + '/followers/'))


    #first account:
    NFollowers1,NFollowing1 = findNumberOfFollowersAndFollowing(driver)
    follAmount1 = NFollowers1 + NFollowing1

    driver.get('https://www.instagram.com/accounts/login/?next=/' + account2 + '/followers/')
    WebDriverWait(driver, 20).until(
        EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + account2 + '/followers/'))

    #second account:
    NFollowers2, NFollowing2 = findNumberOfFollowersAndFollowing(driver)
    follAmount2 = NFollowers2 + NFollowing2

    if (follAmount1>follAmount2):
        account = 2
        followersAmount = NFollowers2
        followingAmount = NFollowing2
    else:
        account = 1
        driver.get('https://www.instagram.com/accounts/login/?next=/' + account1 + '/followers/')
        WebDriverWait(driver, 20).until(
            EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + account1 + '/followers/'))
        followersAmount = NFollowers1
        followingAmount = NFollowing1

    # click on followers
    followers_btn = driver.find_elements_by_class_name('g47SY')
    followers_btn[1].click()

    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # find the followers window
    dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]')

    elem = driver.find_element_by_xpath('//*[@class="FPmhX notranslate _0imsa "]')
    time.sleep(2)
    for i in range(0, 6):
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_DOWN)

    # scroll down the page
    num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
    while (int(followersAmount) != num):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000) / 1000)
        num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
        a = os.system('CLS')
        print("Extracting friends {} of {} ({}%)".format(num, followersAmount, round((num / followersAmount) * 100, 2)))

    followers = BeautifulSoup(driver.page_source, features="lxml").find_all("a", {'class': 'FPmhX notranslate _0imsa '})
    found = 0
    if (account == 1):
        for follower in followers:
            if follower.get_text() == account2:
                found = 1
                break
    elif (account == 2):
        for follower in followers:
            if follower.get_text() == account1:
                found = 1
                break

    if (found == 0):
        return False

    driver.back()

    # click on following
    followers_btn = driver.find_elements_by_class_name('g47SY')
    followers_btn[2].click()

    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # find the following window
    dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]')

    elem = driver.find_element_by_xpath('//*[@class="FPmhX notranslate _0imsa "]')

    elem.send_keys(Keys.PAGE_UP)
    time.sleep(3)
    for i in range(0, 6):
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_DOWN)

    # scroll down the page
    num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()

    while (int(followingAmount) != num):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000) / 1000)
        num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
        a = os.system('CLS')
        print("Extracting friends {} of {} ({}%)".format(num, followingAmount, round((num / followingAmount) * 100, 2)))

    following = BeautifulSoup(driver.page_source, features="lxml").find_all("a", {'class': 'FPmhX notranslate _0imsa '})

    if (account == 1):
        for follower in following:
            if follower.get_text() == account2:
                return True
    elif (account == 2):
        for follower in following:
            if follower.get_text() == account1:
                return True

    return False


def getFollowers(account,driver):
    data["url"] = 'https://www.instagram.com/' + account + '/followers/'
    driver.get(data["url"])
    driver.maximize_window()

    WebDriverWait(driver, 20).until(
        EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + account + '/followers/'))

    # click on followers
    followers_btn = driver.find_elements_by_class_name('g47SY')
    followers_btn[1].click()

    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # find the followers window
    dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]')

    # find number of followers
    follamount = driver.find_element_by_xpath("//li[2]/a/span").text

    follamount = follamount.replace(',', "")

    if 'k' in follamount:
        follamount = follamount[:-1]
        follamount = int(float(follamount)) * 1000

    else:
        follamount = int(float(follamount))

    elem = driver.find_element_by_xpath('//*[@class="FPmhX notranslate _0imsa "]')

    time.sleep(2)
    for i in range (0,6):
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_DOWN)


    # scroll down the page
    num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
    while (int(follamount) != num):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000) / 1000)
        num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
        a = os.system('CLS')
        print("Extracting friends {} of {} ({}%)".format(num, follamount, round((num / follamount) * 100, 2)))

    followers = BeautifulSoup(driver.page_source, features="lxml").find_all("a", {'class': 'FPmhX notranslate _0imsa '})
    followers_arr = []
    for follower in followers:
        followers_arr.append(follower.get_text())

    return followers_arr


def getFollowing(account,driver):
    data["url"] = 'https://www.instagram.com/' + account + '/followers/'
    driver.get(data["url"])
    driver.maximize_window()

    WebDriverWait(driver, 20).until(
        EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + account + '/followers/'))

    # click on following
    followers_btn = driver.find_elements_by_class_name('g47SY')
    followers_btn[2].click()

    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

    # find the following window
    dialog = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]')

    # find number of following
    follamount = driver.find_element_by_xpath("//li[3]/a/span").text

    follamount = follamount.replace(',', "")

    if 'k' in follamount:
        follamount = follamount[:-1]
        follamount = int(float(follamount)) * 1000

    else:
        follamount = int(float(follamount))

    elem = driver.find_element_by_xpath('//*[@class="FPmhX notranslate _0imsa "]')

    time.sleep(2)
    for i in range (0,6):
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_UP)
        elem.send_keys(Keys.PAGE_DOWN)


    # scroll down the page
    num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
    while (int(follamount) != num):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        time.sleep(random.randint(500, 1000) / 1000)
        num = driver.find_elements_by_xpath('//*[@class="FPmhX notranslate _0imsa "]').__len__()
        a = os.system('CLS')
        print("Extracting friends {} of {} ({}%)" .format(num,follamount,round((num / follamount) * 100, 2)))

    followers = BeautifulSoup(driver.page_source, features="lxml").find_all("a", {'class': 'FPmhX notranslate _0imsa '})
    followers_arr = []
    for follower in followers:
        followers_arr.append(follower.get_text())

    return followers_arr


def calcTfIdf(index):

    queryWords= ["draw", "drawing", "drawings", "art", "artist", "artists", "artwork", "paint", "painting", "paintings"]

    #constructing tf:

    accounts = []

    for accountWords in index:
        terms = []
        for word in accountWords["words"]:
            if word["word"] in queryWords:
                term = {
                    "account" : accountWords["account"],
                    "word" : word["word"],
                    "tf" : word["count"]/accountWords["wordsTotal"],
                    "df" : 0,
                    "idf" : 0,
                    "tf-idf" : 0
                }
                terms.append(term)
        accounts.append(terms)

    # constructing df:

    for account in accounts:
        for term in account:
            for accountWords in index:
                if word in accountWords["words"]:
                    term["df"] += 1

            if (term["df"] != 0):
                term["idf"] = math.log10(len(index) / term["df"])
            else:
                term["idf"] = 0

            # calculating tf-idf:
            term["tf-idf"] = term["tf"] * term["idf"]
            print("For the term '{}' in the profile '{}' tf-idf = {} ".format(term["word"],term["account"], term["tf-idf"]))

    return accounts


def writeTfIdfToExcel(accounts, fileName):

    xbook = xlsxwriter.Workbook("C:/Users/inbar/Desktop/" + fileName + ".xlsx")
    xsheet = xbook.add_worksheet("sheet1")
    xsheet.set_column(0, 1, 100)

    row = 0

    for account in accounts:
        for term in account:
            string = "For the term '" + term["word"] + "' in the profile '" + term["account"] + "' tf-idf = " + str(term["tf-idf"])
            xsheet.write(row, 0, string)
            row += 1

    xbook.close()


def writeWordCountToExcel(data, fileName):

    xbook = xlsxwriter.Workbook("C:/Users/inbar/Desktop/" + fileName + ".xlsx")
    xsheet = xbook.add_worksheet("sheet1")
    xsheet.set_column(0, 100, 15)

    column = 0

    for word in data:
        xsheet.write(0, column, word["word"])
        xsheet.write(1, column, word["count"])
        column+=1
    xbook.close()

def writeIndexToExcel(words, accounts, fileName):

    xbook = xlsxwriter.Workbook("C:/Users/inbar/Desktop/" + fileName + ".xlsx")
    xsheet = xbook.add_worksheet("sheet1")
    xsheet.set_column(0, 100, 20)

    words = words[:15]
    words = sorted(words, key=itemgetter('word'), reverse=False)
    data = []

    for account in accounts:
        accountWords = {
            "account" : account["account"],
            "wordsArr" : []
        }
        for word in account["words"]:
            accountWords["wordsArr"].append(word["word"])

        data.append(accountWords)

    print(data)

    row = 0

    for word in words:
        xsheet.write(row, 0, word["word"])
        column = 2
        for accountWords in data:
            xsheet.write(row, 1, "->")
            for y in accountWords["wordsArr"]:
                if (word["word"] == y):
                    xsheet.write(row, column, accountWords["account"])
                    column += 1
        row+=1


    xbook.close()


def writeAccountsToExcel(followArr, fileName):

    xbook = xlsxwriter.Workbook("C:/Users/inbar/Desktop/" + fileName + ".xlsx")
    xsheet = xbook.add_worksheet("sheet1")
    xsheet.set_column(0,100,20)

    column = 0

    for account in followArr:
        xsheet.write(1, column, account)
        column += 1

    xbook.close()

def findWord(accountWords, word):

    wordsArr = accountWords["words"]

    for wordi in wordsArr:
        if (wordi["word"]==word):
            return wordi

    return -1


def getWords(driver, list):

    index =[]

    for follower in list:
        url = 'https://www.instagram.com/' + follower + '/'
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.url_changes('https://www.instagram.com/accounts/login/?next=/' + follower + '/'))

        waiter.find_element(driver, '//*[@class="-vDIg"]', by=XPATH)
        try:
            accountWords = re.split('[^a-zA-Z]', driver.find_element_by_xpath('//*[@class="-vDIg"]/span').text)
            accountWords = [word.translate(str.maketrans('','',string.punctuation)).lower()
                            for word in accountWords if ((word not in stopwords.words('english'))and word!="")]
        except NoSuchElementException:
            continue

        accountWordsD ={
            "account": follower,
            "wordsTotal": len(accountWords),
            "words": []
        }
        for word in accountWords:
            newWordAccount = {
                "word": word,
                "count": 1
            }

            temp1 = findWord(accountWordsD,newWordAccount["word"])
            if (temp1 == -1):
                accountWordsD["words"].append(newWordAccount)
            else:
                temp1["count"]+=1

            newWord = {
                "word": word,
                "count": 1
            }

            if (('words' not in locals())):
                words = [newWord]
            else:
                temp = next((item for item in words if item["word"] == word),-1)
                if(temp ==-1):
                    words.append(newWord)
                else:
                    temp['count']+=1

        index.append(accountWordsD)

    words = (sorted(words, key=itemgetter('count'), reverse=True))

    print(words)
    print(index)

    return words, index


def login(driver):
    data["url"] = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    driver.get(data["url"])
    driver.implicitly_wait(3)

    username = driver.find_element_by_xpath('//*[@name="username"]')
    password = driver.find_element_by_xpath('//*[@name="password"]')
    login_btn = driver.find_element_by_xpath('//*[@class="_0mzm- sqdOP  L3NKy       "]')

    username.send_keys(data["username"])
    password.send_keys(data["password"])

    # login
    login_btn.click()

# Main:
login_details = input("Please enter your name and password: ").split(" ")
data["username"] = login_details[0]
data["password"] = login_details[1]

driver = webdriver.Chrome()
login(driver)
driver.minimize_window()

while (True):
    action = input("\nWhich of the following would you like to do?(enter the action's number)\n"
                   "1. Find common followers of two accounts\n"
                   "2. Find common following of two account\n"
                   "3. Search for a certain user in the list of another user's followers\n"
                   "4. Search for a certain user in the list of another user's following\n"
                   "5. Check if two user's follow each other\n"
                   "6. Exit\n\n")

    if (action == '1'):
        accounts = input("Please enter both usernames separated by a space: ").split(" ")
        account1followers = getFollowers(accounts[0], driver)
        account2followers = getFollowers(accounts[1], driver)
        mutual = []
        for follower in account1followers:
            for follower2 in account2followers:
                if follower == follower2:
                    mutual.append(follower)
                    break
        print(mutual)
        words, index = getWords(driver, mutual)
        writeAccountsToExcel(mutual, "Common Followers (inbaral & inbaral_)")
        writeWordCountToExcel(words, "words count common followers")
        writeIndexToExcel(words, index, "index common followers")


    elif (action == '2'):
        accounts = input("Please enter both usernames separated by a space: ").split(" ")
        account1following = getFollowing(accounts[0], driver)
        account2following = getFollowing(accounts[1], driver)
        mutual = []
        for follower in account1following:
            for follower2 in account2following:
                if follower == follower2:
                    mutual.append(follower)
                    break
        print(mutual)
        words, index = getWords(driver, mutual)
        writeAccountsToExcel(mutual, "Common Following (inbaral & inbaral_)")
        writeWordCountToExcel(words, "words count following")
        writeIndexToExcel(words, index, "index common following")
        writeTfIdfToExcel(calcTfIdf(index), "tf-idf to common following (inbaral & inbaral_")

    elif (action == '3'):
        account = input("Please enter the account in which you would like to look: ")
        user = input("Enter the name of the user you would like to look for: ")
        account1followers = getFollowers(account, driver)
        flag = 0
        for follower in account1followers:
            if follower == user:
                flag = 1
                print("Yes. {} follows {}\n".format(user, account))
                break
        if flag == 0:
            print("No. {} does not follow {}\n".format(user, account))


    elif (action == '4'):
        account = input("Please enter the account in which you would like to look: ")
        user = input("Enter the name of the user you would like to look for: ")
        account1followers = getFollowing(account, driver)
        flag = 0
        for follower in account1followers:
            if follower == user:
                flag = 1
                print("Yes. {} is in {}'s following list\n".format(user, account))
                break
        if flag == 0:
            print("No. {} is not in {}'s following list\n".format(user, account))

    elif (action == '5'):
        account1, account2 = input(
            "Please enter the accounts you would like to check mutual following for, separated by a spase: ").split(" ")
        if (isMutual(account1, account2, driver)):
            print("{} and {} mutually follow each other\n".format(account1, account2))
        else:
            print(print("{} and {} do not mutually follow each other\n".format(account1, account2)))
    elif (action == '6'):
        driver.quit()
        break



