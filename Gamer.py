from bs4 import BeautifulSoup
import pynotify
import requests

def main():
	r = requests.get("http://gameloot.in/product-category/pre-owned/?swoof=1&pa_platforms=ps3&really_curr_tax=50-product_cat")
	data = r.text
	soup = BeautifulSoup(data)
	
	pynotify.init('test')
	pynotify.init("Basic")
	
	finalgamelist= getgamename(soup)
	finallist = getprice(soup)

	for i,row in enumerate(finalgamelist):
		n = pynotify.Notification("Gameloot",row + finallist[i])	
		n.show()

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
	

if __name__ == '__main__':
	main()