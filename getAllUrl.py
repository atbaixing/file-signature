# 获取所有需要爬取的url
from urllib import request
from bs4 import BeautifulSoup
import json
# ssl协议需要
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urlList = []


def getUrl(pageIndex):
  url = "https://filesignatures.net/index.php?page=all&&order=EXT&alpha=All&currentpage=" + pageIndex
  headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
  req=request.Request(url=url,headers=headers)
  response=request.urlopen(req)

  html=response.read()
  html=html.decode("utf-8")

  # 解析网页
  # 解析器需要手动安装 pip install lxml
  bs = BeautifulSoup(html, 'lxml')

  rowEles = bs.select('#innerTable>tr')

  for rowEle in rowEles[1:]:
    url = rowEle.find_all('td')[2].select('span>a')[0].get('href')
    urlList.append('https://filesignatures.net'+ url)
  
# 保存数据
def writeData(obj):
  with open('./data/url_list.json', 'w') as fileObj:
    json.dump(obj, fileObj)

# 爬取url
if __name__=="__main__":
  for i in range(18):
    getUrl(str(i+1))
  
  print(len(urlList))
  writeData(urlList)
