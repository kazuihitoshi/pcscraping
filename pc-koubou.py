# coding: UTF-8
import urllib.request,urllib.error
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser
import urllib.parse 

import linkshare
import secure_linkshareuserdata

targeturl ="https://www.pc-koubou.jp/pc/osless_style_note.php"
outputfile = "pc-koubou.html"
ecsiteid = '13526' #パソコン工房
urltimeout = 60
options = Options()
options.add_argument('--headless')

def cVal(src):
        ret=src.replace('円','')
        ret=ret.replace(' ','')
        ret=ret.replace('\n','')
        ret=ret.replace(',','')
        ret=int(ret)
        return(ret)

def pclist(soup,baseurl):
        list=[]
        cnt = 0
        err = None
        for bs2 in soup.select('div.search-result'):
                ret = {}
                try:
                    d = bs2.find('a',{'target':'_blank'}) 
                    if d is not None:
                        ret['url'] = urljoin(baseurl,d.get("href"))
                except Exception as e:
                        err=e
                try:                        
                        ret['note']=bs2.find('div',{'class':'spec'}).get_text()
                        ret['note']=ret['note']+bs2.find('div',{'class':'price-opt'}).get_text()
                except Exception as e:
                        err=e                                
                try:                        
                        ret['price']=bs2.find('span',{'class':'price--num'}).get_text()
                        ret['price']=cVal(ret['price'])

                except Exception as e:
                        err=e
                try:
                        ret['productname']=bs2.find('p',{'class':'name'}).get_text()
                except Exception as e:
                        err=e
                
                try:
                        ret['imageurl']=urljoin(baseurl,bs2.find('img',{'class':'SJ-image'})['src'])
                except Exception as e:
                        err=e

                list.append(ret)
        return ( list )

browser = webdriver.Chrome(chrome_options=options)
browser.implicitly_wait(3)

browser.get(targeturl)
soup = BeautifulSoup(browser.page_source,'html.parser')
osless=pclist(soup,targeturl)

f = open(outputfile,encoding="utf-8",mode="w")
osless = sorted(osless, key=lambda x:x['price'])
aff = linkshare.open(secure_linkshareuserdata.linkshare_user,secure_linkshareuserdata.linkshare_pass)

for a in osless:
        afflink = linkshare.getlink(aff,
                ecsiteid,
                a.get('url'),
                a.get('imageurl'),
                a.get('productname'))
        d = a.get('productname')
        if d is not None :
                f.write('<div class="row boxin">\n')
                f.write(' <div class="col-12 productname">' )             
                dd = afflink.get('textlink')

                if dd is not None:
                        f.write(dd)
                else:
                        f.write( d )
                
                f.write('</div>\n')
        
                dd = afflink.get('imagelink')
                if dd is not None:
                        f.write(' <div class="col-4">' + dd + '</div>' )
                
                f.write(' <div class="col-8">\n')
                f.write('         <div class="row">\n')
                d = a.get('price')
                if d is not None:
                        f.write('                 <div class="col-12">価格:'+'{:,}'.format(d)+'円</div>\n' )
                d = a.get('note')
                if d is not None:
                        f.write('                 <div class="col-12">特徴:' + d + '</div>\n')
                f.write('         </div>\n')
                f.write(' </div>\n')
                f.write('</div>\n')
f.close()

aff.close()
browser.quit()

