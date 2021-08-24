from bs4 import BeautifulSoup
import requests
import telegram
from telegram import chat
from telegram import message
from hotdeal.models import Deal
from datetime import datetime, timedelta



response=requests.get(
    "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu")

soup = BeautifulSoup(response.text,"html.parser")
BOT_TOKEN ="1994701279:AAH2fCFs_y867mGFZCS8EbF7_h2Q9qHSyo4"

bot = telegram.Bot(token=BOT_TOKEN)

def run():
    
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()

    print(row,"deals deleted")


    for item in soup.find_all("tr",{'class':["list1","list0"]}):
        try:
            image = item.find("img",class_="thumb_border").get("src")[2:]
            image = "http://"+image
            title=item.find("font",class_="list_title").text
            title = title.strip()
            link = item.find("font",class_="list_title").parent.get("href")
            link = "https://www.ppomppu.co.kr/zboard/" + link
            reply_count = item.find("span",class_="list_comment2").text
            reply_count=int(reply_count)
            up_count = item.find_all("td")[-2].text
            up_count = up_count.split("-")[0]
            up_count =int(up_count)
            if up_count >=0:
                if(Deal.objects.filter(link__iexact=link).count( )== 0) :
                    Deal(image_url=image, title=title, link=link, 
                    reply_count=reply_count, up_count=up_count).save()
                    bot.sendMessage(-1001514113152, '{} {}'.format(title,link))
        except Exception as e : 
            continue