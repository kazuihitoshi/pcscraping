# coding: UTF-8
import urllib.request,urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser

# ブラウザのオプションを格納する変数をもらってきます。
#options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
#options.set_headless(True)

# ブラウザを起動する
#driver = webdriver.Chrome(chrome_options=options)

# ブラウザでアクセスする
#driver.get("https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/sc/laptops/vostro-laptops")

# HTMLを文字コードをUTF-8に変換してから取得します。
#html = driver.page_source.encode('utf-8')
#html = urllib.request.urlopen("https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/sc/laptops/vostro-laptops")
html = urllib.request.urlopen("https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/sc/laptops")
# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")
# idがheikinの要素を表示
#print (soup.select_one("#heikin"))
#print (soup.select_one("#category-page > section:nth-child(3) > div"))
#print(pc.find("a"))
#for pc in soup.select_one("#eSeriesVariant > div.clear-both.hidden-xs > div:nth-child(1) > div > ul"):
#    if pc != "\n" :
#        s = BeautifulSoup(pc,"html.parser")
#        for atag in s.find_all("a"):
#                print(atag.string)
#        s.clear
#pcIndex = soup.select_one("#eSeriesVariant > div.clear-both.hidden-xs > div:nth-child(1) > div > ul")
#pcs = pcIndex.find_all("li")
#for pc in soup.select_one("#eSeriesVariant > div.clear-both.hidden-xs > div:nth-child(1) > div > ul").find_all("li"):
#        print(pc.find("a").get("href"))
                           #eSeriesVariant > div.clear-both.hidden-xs > div:nth-child(2)
cnt = 0
for nth_child in soup.select("#eSeriesVariant > div.clear-both.hidden-xs"):
        for doccol in nth_child.find_all("div"):
                for docrow in doccol.find_all("div"):
                        for li in docrow.find("ul").find_all("li"):
                                s=li.find("a")
                                if s != -1 :
                                        cnt+=1
                                        print (s.get("href"))

print("count=" + str(cnt))