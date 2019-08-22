import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Purpose - Automate tracking of Amazon product price and send email alert if lower than desired threshold

#Step 1 - paste URL to amazon product
URL = 'https://www.amazon.com/Dell-9360-Anti-Glare-InfinityEdge-Touchscreen/dp/B074G5DQ5M/ref=sr_1_4?crid=155OPPS71OIMH&keywords=dell+xps+13&qid=1566455651&s=gateway&sprefix=dell+xps%2Caps%2C384&sr=8-4'

#Step 2 - Google "whats my user agent" and copy/paste results below. This change based on pc and browser
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

#function to pull parse data from URL
def check_price():
	page = requests.get(URL, headers=headers)

	content = BeautifulSoup(page.content, 'html.parser')
	content2 = BeautifulSoup(content.prettify(), 'html.parser')
	#identified id="" within html for title and price
	title = content2.find(id="productTitle").get_text()
	title = title.strip()
	price = content2.find(id="priceblock_ourprice").get_text()
	price_string = str(price)
	converted_price = float(price[1:5])

	#print(title)
	print(converted_price)
	
	if(converted_price < 900):
		send_mail(price,URL,title)

#function to send email and pass price, URL and title 
def send_mail(price, URL,title):
	server  = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('XXXXXXX@gmail.com', 'XXXXXXXXXX')

	subject = 'Price change on Amazon item: {}'.format(price)
	body = 'Check out the link {}\n\n{}'.format(URL, title)
	#msg = f"Subject:{subject}\n\n{body}"
	msg = 'Subject: {}\n\n{}'.format(subject,body)

	#sendmail(FROM, TO, msg)
	server.sendmail('XXXXXXXX@gmail.com','XXXXXXXX@gmail.com',msg)
	print('email has been sent!')

	server.quit()

#running script but put to sleep for 24 hrs or 86400 secs
while(True):
	check_price()
	time.sleep(86400)