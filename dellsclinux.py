# coding: UTF-8
import urllib.request,urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser
import urllib.parse 
import datetime 
import secure_linkshareuserdata
import linkshare
import bloggerpost

targeturl ="https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/sc/laptops"
outputfile = "dell.html"
urltimeout = 120
today = datetime.datetime.now().strftime('%Y/%m/%d')

browser = linkshare.open(secure_linkshareuserdata.linkshare_user,secure_linkshareuserdata.linkshare_pass,True)

def gethead(today,totalcount):
        ret ='<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">\n'
        ret+='<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>\n'
        ret+='<div class="separator" style="clear: both; text-align: center;"><a href="https://3.bp.blogspot.com/-6yNB7wFPCTE/XuXJWRHJ--I/AAAAAAAAj9Y/4zSkoQxkqLkVS5FMbearatX-zShMPhWEgCLcBGAsYHQ/s1600/dell%252Bubuntu.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="https://3.bp.blogspot.com/-6yNB7wFPCTE/XuXJWRHJ--I/AAAAAAAAj9Y/4zSkoQxkqLkVS5FMbearatX-zShMPhWEgCLcBGAsYHQ/s320/dell%252Bubuntu.png" width="320" height="192" data-original-width="600" data-original-height="360" /></a></div>\n'
        ret+='<meta name="twitter:card" content="summary_large_image" />\n'
        ret+='<meta name="twitter:site" content="@kazuihitoshi" />\n'
        ret+='<meta property="og:url" content="https://ubuntu84.blogspot.com/2020/05/dellubuntu-2020531.html" />\n'
        ret+='<meta property="og:title" content="Linuxノートパソコンが買える DELL製'+str(totalcount)+'機種 '+today+'更新" />\n'
        ret+='<meta property="og:description" content="DELLサイトで見つけたLinux指定可能なノートパソコン'+str(totalcount)+'機種を掲載しています。" />\n'
        ret+='<meta property="og:image" content="https://3.bp.blogspot.com/-6yNB7wFPCTE/XuXJWRHJ--I/AAAAAAAAj9Y/4zSkoQxkqLkVS5FMbearatX-zShMPhWEgCLcBGAsYHQ/s1600/dell%252Bubuntu.png" />\n'
        ret+='<h2>はじめに</h2>\n'
        ret+='<p>Linuxが搭載されたノートパソコンってなかなかないですよね。デスクトップパソコンやサーバ機であれば販売されているとこありますが、ノートパソコンになるとほとんど無いように思います。</P>\n'
        ret+='<p>ノートパソコンはWindowsが搭載されているものと、ほぼ諦めていたのですが、DELLサイトでOS選択肢にLinuxが表示されるものを見つけまして、一体どの程度の機種に指定できるのか調べてみました。</p>\n'
        ret+='<p>なんと'+str(totalcount)+'機種もLinuxディストリビューションで人気のUbuntuプレインストール指定可能な製品が見つかりました。</p>\n'
        ret+='<p>それも嬉しいことに、Win10Proを選択した場合に比べ約2万円お安く購入可能です。</p>\n'
        ret+='<p>皆様のLinuxライフにお役に立てると嬉しいです。それでは早速行ってみます。</p>\n'
        ret+='<br>\n'
        ret+='<h2>DELLで買えるLinux(Ubuntu)プレインストールパソコン</h2>\n'
        ret+='<p>'+today+'の情報です。'+str(totalcount)+'機種を安価な順に並べています。</p>\n'        
        return(ret)

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
if True :
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

#linuxproduct.append({'productname': '【Dell】Dell Latitude 350', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': -19600, 'price': 211700,'realprice':100})

#linuxproduct.append(checkLinuxAndGetPage('https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-5501/spd/latitude-15-5501-laptop/al5501'))
#linuxproduct.append({'productname': 'Latitude 3300', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': -19600, 'price': 211700,'realprice':100})
#linuxproduct.append({'productname': 'Latitude 3300', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': -19600, 'price': 211700,'realprice':100})
#linuxproduct.append({'productname': 'Latitude 33xxx', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': -19600, 'price': 211700,'realprice':100})
#linuxproduct.append({'productname': 'Latitude 3300', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': -19600, 'price': 211700,'realprice':100})
#linuxproduct.append({'productname': 'Dell Latitude 7310', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7310/spd/latitude-13-7310-2-in-1-laptop/al7310', 
#'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/cs2004g0010-68001-latitude-family-fy21-7000series-thumbnail.jpg', 'linuxprice': '- 19,600円', 
#'price': '211,700円','realprice':100})
#linuxproduct.append({'productname': 'Dell Latitude 7300', 'url': 'https://www.dell.com/ja-jp/work/shop/%E3%83%87%E3%83%AB%E3%81%AE%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3/dell-latitude-7300/spd/latitude-13-7300-laptop/al7300', 'imageurl': 'https://i.dell.com/sites/csimages/Video_Imagery/all/latitude-7000-new.jpg', 'linuxprice': '- 19,600円', 'price': '\n            205,200円\n        ','realprice':100})
#linuxproduct.append({'productname': 'Dell Latitude 3500','realprice':100})

if True :
	f = open(outputfile,encoding="utf-8",mode="w")
	linuxproduct = sorted(linuxproduct, key=lambda x:x['realprice'])
	h = gethead(today,len(linuxproduct)+1)
	f.write(h)
	for a in linuxproduct:
		d = a.get('productname')
		#print('d:'+d)
		aff =linkshare.getlinkfinder(browser,'2557',d)
		#print('d:'+d)
		#print(aff)

		if d is not None :
			f.write('<div class="row box">\n')
			f.write(' <div class="col-12 productname">' )
			
			dd = a.get('url')
			#print( 'dd:'+dd )

			if dd is not None:
				if aff.get('url') != '':
					f.write(aff.get('url'))
				else:
					f.write('<a href="' + dd + '">'+d+'</a>')
			else:
				f.write( d )
			
			f.write('</div>\n')
		
		 
			if dd is not None:
				f.write(' <div class="col-4">\n' )
				if aff.get('imageurl') != '':
					f.write(aff.get('imageurl'))
				else:
					f.write('<a href="' + dd +'">\n')
					d = a.get('imageurl')
					if d is not None:
						f.write('<img src="'+d+'" width="100%">\n')
					f.write('</a>\n')
				f.write('</div>\n')
			
			f.write(' <div class="col-8">\n')
			f.write('         <div class="row">\n')
			d = a.get('price')
			if d is not None:
				f.write('                 <div class="col-12">価格:' + '{:,}'.format(d) + '円</div>\n' )
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

linkshare.close(browser)

if True :
	body=open('dell.html',encoding='utf-8',mode='r').read()
	p = bloggerpost.open()
	title='Linuxノートパソコンが買える DELL製'+str(len(linuxproduct)+1)+'機種 '+today+'更新'
	bloggerpost.update(posts=p,postId='7870701470902384798',title=title,body=body)

