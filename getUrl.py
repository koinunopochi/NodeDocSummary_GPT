import requests
from bs4 import BeautifulSoup

#URLを指定
url = "https://nodejs.org/api/index.html"

#GETリクエストを送信
reqs = requests.get(url)

#URLをテキスト化し、解析を行う。その後BeautifulSoupオブジェクトを作る
soup = BeautifulSoup(reqs.text, 'html.parser')

#空のurlsのリストを用意
urls = []

#全てのaタグをループ処理し、hrefで指定されたURLを出力する
for link in soup.find_all('a'):

    #print(link.get('href'))
    urls.append(link.get('href'))

#urlsのリストを表示
print(urls)

#urlsのリストをテキストファイルに書き込む
f = open('list.js', 'w')
f.write("const urls = [")
for x in urls:
    if(x in "https://"):
        f.write("'"+str(x) + "',")
    else:
        f.write("'https://nodejs.org/api/"+str(x) + "',")
f.write("]")
f.close()
