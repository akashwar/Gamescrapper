from bs4 import BeautifulSoup
import pynotify
import requests
import sys

def main():
	
	pynotify.init('test')
	
	platform = raw_input("Enter the platform to search (ps4,ps3,xbox-one,xbox-360):")

	for i in range(1,6):
		url = "http://gameloot.in/product-category/pre-owned/page/" + str(i) + "/?swoof=1&pa_platforms=" + platform + "&really_curr_tax=50-product_cat" 
		r = requests.get(url,verify=False)
		data = r.text
		soup = BeautifulSoup(data,"lxml")
		notify(soup)

	pass
	
def notify(soup):
	finalgamelist= getgamename(soup)
	finallist = getprice(soup)
	finalstockstate = getstockstatus(soup)
     
	res = "" 

	for i,row in enumerate(finalgamelist):
			res = res + row	+ finallist[i] + " " + finalstockstate[i].upper()  + "\n"
	if res:
		n = pynotify.Notification("Gameloot",res)
		n.set_timeout(10000)	
		n.show()
 
	pass


def getgamename(soup):
	extractedgame = soup.select('div.product_details')
	extractedprice = soup.select("ins")
	gamelist=[]
	for i,row in enumerate(extractedgame):
		gamelist.append(row.text.split('\n')[2])

	return gamelist
	

def getprice(soup):
	finallist=[]
	extractedprice = soup.find_all('span',{"class":"product_price headerfont"})
	for i in extractedprice:
		if i.findAll('del'):
			 tg=i.find('ins').contents[0]
			 finallist.append(tg.text)
		else:
			 finallist.append(i.text)

	return finallist
	
def getstockstatus(soup):
	extractedstock = []
	extracted = soup.find_all('div',{"class":"tcol-md-3 tcol-sm-4 tcol-xs-6 tcol-ss-12 kad_product"})
	for i in extracted:
		temp = i.find('div',{"class":"in-stock"})
		if not temp:
			extractedstock.append("#Out of stock")
		else:
			extractedstock.append("#" + temp.contents[0])

	return extractedstock

if __name__ == '__main__':
	main()
