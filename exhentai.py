import requests
from bs4 import BeautifulSoup
import requests.packages.urllib3
import os
import GUI
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
requests.packages.urllib3.disable_warnings()

# 實用 容易套用至其他爬蟲
# cookie字串轉字典化
def cookie():
	f = open(r'cookie.txt' , 'r')
	cookies = {}
	for line in f.read().split(';'):
		name, value = line.strip().split('=', 1)
		cookies[name] = value
	f.close()
	return cookies

# 拿書名
def get_title(soup):
	title = soup.find("h1", id='gj')
	book_name = title.get_text()
	return book_name

# 算有幾頁，一頁40張那種，不是總頁數
def max_page(soup):
	change_bpage = soup.find_all("td",onclick="document.location=this.firstChild.href")
	max_page = int(change_bpage[-2].text)
	return max_page

# 用書名創建資料夾，並取得路徑
def mkdir(book_name):
	path = './magic_index' + '/' + book_name
	if os.path.exists(path):
		return path
	else:
		os.makedirs(path)
		return path

# 送出request，並用美麗湯整理html
def get_soup(url,headers,cookies):
	i = 0
	while i < 3:
		try:
			r = requests.get(url=url,headers=headers,timeout=10,verify=False, cookies=cookies)
			html = r.text
			soup = BeautifulSoup(html,'html.parser')
			return soup
		except requests.exceptions.RequestException as e:
			print(e)
			i += 1

# 從每一頁漫畫取得原始圖片連結
def get_img_data(soup):
	comic = soup.find('img',id='img')
	img = comic.get('src')
	img_data = requests.get(img).content
	return img_data

# 獲取每一頁的連結，單行本200+的那種頁
def get_page_link(soup,pages,url,headers,cookies):
	alink = soup.find_all("div" ,class_ = "gdtm")
	aalink = []
	hlink = []
	for i in range (0,40):
		aalink += alink[i].select('a')
		hlink.append(aalink[i].get('href'))
	for i in range(1,pages):
		soup2 = get_soup((url + '?p=' + str(i)),headers,cookies)
		alink2 =soup2.find_all("div" ,class_ = "gdtm")
		aalink = []
		count = -1
		for j in alink2:
			count += 1
			aalink += j.select('a')
			hlink.append(aalink[count].get('href'))
	return hlink

# 下載每一頁漫畫
def download_comic(page, count, headers, cookies,path):
	soup = get_soup(page,headers,cookies)
	img_data = get_img_data(soup)
	with open('%s/%s.jpg' %(path,str(count)), 'wb') as f:
		f.write(img_data)
	print('picture ' + str(count) + ' done')

def downloader_a(url):
	cookies = cookie()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
	}
	soup = get_soup(url, headers, cookies)
	book_name = get_title(soup)
	pages = max_page(soup)
	path = mkdir(book_name)
	link = get_page_link(soup, pages, url, headers, cookies)
	# 開始下載
	str = '開始下載: ' + book_name
	GUI.print_output(str)
	count = 0
	for page in link:
		count += 1
		download_comic(page, count, headers, cookies, path)
	print('done : ' + book_name)

def downloader_b(url, start_page):
	cookies = cookie()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
	}
	soup = get_soup(url, headers, cookies)
	book_name = get_title(soup)
	pages = max_page(soup)
	path = mkdir(book_name)
	link = get_page_link(soup, pages, url, headers, cookies)
	# 開始下載
	print('start : ' + book_name)

	end_page = len(link)
	count = start_page - 1
	for page in range(start_page-1,end_page):
		count += 1
		download_comic(link[page],count,headers,cookies,path)
	print('done : ' + book_name)







