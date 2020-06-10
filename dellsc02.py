# coding: UTF-8
import urllib.request,urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser
import urllib.parse 

targeturl ="https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/sc/laptops"
outputfile = "dell.html"
urltimeout = 60
def pclist(soup):
        list=[]
        cnt = 0
        for nth_child in soup.select("#cat-content-container > div.cat-off-screen-pane"):
                for doccol in nth_child.find_all("div",{'class':'fran'}):
                        for docrow in doccol.find_all("div",{'class':'ser'}):
                                for li in docrow.find("ul").find_all("li"):
                                        s=li.find("a")
                                        if s != -1 :
                                                cnt+=1
                                                list.append('https:'+urllib.parse.quote(s.get("href")))
                                                #print (s.get("href")+':'+s.get_text())
        return ( list )

def cVal(src):
        ret=src.replace('円','')
        ret=ret.replace(' ','')
        ret=ret.replace('\n','')
        ret=ret.replace(',','')
        ret=int(ret)
        return(ret)

def checkLinuxAndGetPage(urlstring):
        ret = {}
        err = 0
        bs2 = BeautifulSoup(urllib.request.urlopen(urlstring,timeout=urltimeout),"html.parser")
        for opt in bs2.find_all("div",{'class':'cf-opt-wrap'}): #bs2.find_all("input",{'type':'radio'}): #
                lo = opt.find("input",{'type':'radio'})
                if lo is not None:
                        lo = lo.get('aria-label') #opt.get_text().lower()
                if lo is not None:
                        lo = lo.lower()
                        if lo.find('linux') > 0 or lo.find('ubuntu') >0 :
                                ret['url'] = urlstring
                                try:                        
                                        ret['note']=bs2.find('ul',{'class':'cf-hero-bts-list'}).get_text()
                                except Exception as e:
                                        err=e                                
                                try:                        
                                        ret['price']=bs2.find('div',{'class':'cf-hero-price'}).find('div',{'class':'cf-dell-price'}).find('div',{'class':'cf-price'}).get_text()
                                        ret['price']=cVal(ret['price'])

                                except Exception as e:
                                        err=e
                                try:
                                        ret['linuxprice']=opt.find("div",{'class':'cf-opt-price'}).find("span").get_text()
                                        ret['linuxprice']=cVal(ret['linuxprice'])
                                        ret['realprice'] = ret['price'] + ret['linuxprice']
                                except Exception as e:
                                        err=e
                                try:
                                        ret['productname']=bs2.find('h1',{'class':'cf-pg-title'}).find('span').get_text()
                                except Exception as e:
                                        err=e
                                
                                try:
                                        ret['imageurl']='https:' + bs2.find('div',{'class':'cf-hero-imaging-section'}).find('img')['src']
                                except Exception as e:
                                        err=e

                                break
        return (ret)

#print(checkLinuxAndGetPage("https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310"))

#----- get webpage data
linuxproduct = []
for a in pclist(BeautifulSoup(urllib.request.urlopen(targeturl), "html.parser")):
        #print (a)
        bs = BeautifulSoup(urllib.request.urlopen(a,timeout=urltimeout), "html.parser")
        for sec in bs.find_all("section",{'class':'ps-top'}):
                linuxflag = 0
                url='https:' + urllib.parse.quote(sec.find("a",{'class':'dellmetrics-iclickthru'}).get("href"))
                getdat = checkLinuxAndGetPage(url)

                if len(getdat) > 0:
                        linuxproduct.append(getdat)  
#                        print (getdat)

#linuxproduct.append(checkLinuxAndGetPage('https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-5501/spd/latitude-15-5501-laptop/al5501'))
#linuxproduct.append({'productname': 'Dell Latitude 7310', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': '- 19,600円', 'price': '\n            211,700円\n        '})
#linuxproduct.append({'productname': 'Dell Latitude 7300', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7300/spd/latitude-13-7300-laptop/al7300', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/latitude-7000-new.jpg', 'linuxprice': '- 19,600円', 'price': '\n            205,200円\n        '})
#linuxproduct.append({'productname': 'Dell Laaaaaatitude 7300'})

f = open(outputfile,encoding="utf-8",mode="w")
linuxproduct = sorted(linuxproduct, key=lambda x:x['realprice'])
for a in linuxproduct:
        d = a.get('productname')
        if d is not None :
                f.write('<div class="row box">\n')
                f.write(' <div class="col-12 productname">' )
                
                dd = a.get('url')

                if dd is not None:
                        f.write('<a href="' + dd + '">'+d+'</a>')
                else:
                        f.write( d )
                
                f.write('</div>\n')
        
         
                if dd is not None:
                        f.write(' <div class="col-4"><a href="' + dd +'">\n' )
                        d = a.get('imageurl')
                        if d is not None:
                                f.write('<img src="'+d+'" width="100%">\n')
                        f.write('</a></div>\n')
                
                f.write(' <div class="col-8">\n')
                f.write('         <div class="row">\n')
                d = a.get('price')
                if d is not None:
                        f.write('                 <div class="col-12">価格:'+'{:,}'.format(d)+'円</div>\n' )
                d = a.get('linuxprice')
                if d is not None:
                        f.write('                 <div class="col-12">Linux選択で:' + '{:,}'.format(d) + '円の' + '{:,}'.format(a.get('realprice'))+'円</div>\n')
                d = a.get('note')
                if d is not None:
                        f.write('                 <div class="col-12">特徴:' + d + '</div>\n')
                f.write('         </div>\n')
                f.write(' </div>\n')
                f.write('</div>\n')
f.close()