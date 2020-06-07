from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from html.parser import HTMLParser
import urllib.request,urllib.error

import time

targeturl = 'https://www.linkshare.ne.jp/'
deeplink = 'https://cli.linksynergy.com/cli/publisher/links/deeplinks.php'

def open(user, pas, headless=True):
    options = Options()

    if headless:
        add_argument('--headless')

    browser = webdriver.Chrome(chrome_options=options)
    browser.implicitly_wait(3)

    browser.get(targeturl)
    textbox=browser.find_element_by_id('Lid')
    textbox.clear()
    textbox.send_keys(user)

    textbox=browser.find_element_by_id('Lpas')
    textbox.clear()
    textbox.send_keys(pas)

    frm=browser.find_element_by_name("loginboxform")
    frm.submit()

    handle_array = browser.window_handles

    browser.switch_to.window(handle_array[1])
    browser.save_screenshot('linkshare_login.png')

    return(browser)

def getlink(browser,ecsiteid,url,imageurl,textmessage):
    ret = {}
    browser.get(deeplink)

    sel = Select(browser.find_element_by_id('advertiserSelect'))
    sel.select_by_value(ecsiteid) #13526:パソコン工房

    #get text link
    sel = browser.find_element_by_id('singleTypeRadio2')
    sel.click()

    sel = browser.find_element_by_id('urlInput')
    sel.clear()
    sel.send_keys(url)

    sel = browser.find_element_by_id('txtLinkTextInput')
    sel.clear()
    sel.send_keys(textmessage)

    sel = browser.find_element_by_css_selector('.showSingle > input')
    sel.submit()
    
    sel = browser.find_element_by_css_selector('.linkHtmlCode')

    ret['textlink'] = sel.text

    #リセット
    sel = browser.find_element_by_css_selector('.showResults')
    sel.submit()

    #get image link
    sel = browser.find_element_by_id('singleTypeRadio3')
    sel.click()

    sel = browser.find_element_by_id('urlInput')
    sel.clear()
    sel.send_keys(url)
    
    sel = browser.find_element_by_id('imgLinkUrlInput')
    sel.clear()
    sel.send_keys(imageurl)
    
    sel = browser.find_element_by_css_selector('.showSingle > input')
    sel.submit()

    sel = browser.find_element_by_css_selector('.linkHtmlCode')

    ret['imagelink'] = sel.text

    #リセット
    sel = browser.find_element_by_css_selector('.showResults')
    sel.submit()

    return(ret)

def close(browser):
    browser.quit()


#browser.save_screenshot('merchant_list.png')

#print(browser.current_url)
#print("必要情報を入力してログインボタンを押下しました")
#time.sleep(6)
#print(browser.current_url)
#browser.quit()