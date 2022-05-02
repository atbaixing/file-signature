# 根据url爬取需要的数据
from urllib import request
from bs4 import BeautifulSoup
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

filetypes=[]

def getPageHtml(url):
  headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
  req=request.Request(url=url,headers=headers)
  response=request.urlopen(req)

  html=response.read()
  html=html.decode("utf-8")
  return html

# 去除空白节点
def trimSpace(s):
  return "".join(s.split())


def getData(url):
  # 获取页面
  html = getPageHtml(url)
  # 转换成bs对象
  bs = BeautifulSoup(html, 'lxml')
  # 通过bs对象接口爬取数据
  rowEles = bs.select('#innerTable>tr')
  # 列表前两行分别为空和表头，列表前两条
  extension_name=''
  rowFlag = True
  
  infoDict = {}
  for rowEle in rowEles[2:]:
    if rowFlag:
      # 第一行获取的数据
      infoDict['extension_name'] = rowEle.find_all('td')[1].select('span>a')[0].string
      infoDict['extension_sig'] = rowEle.find_all('td')[2].select('span>a')[0].string
      infoDict['extension_desc'] = rowEle.find_all('td')[3].string


    else:
      # 第二行需要获取的数据
      item_string = rowEle.find_all('td')[3].getText()
      items = item_string.split('\n')
      for item in items:
        item = trimSpace(item)
        extension_infos = item.split(':')
        if extension_infos[0] == 'Sizet':
          infoDict['extension_sizet'] = extension_infos[1]
        if extension_infos[0] == 'Offset':
          infoDict['extension_offset'] = extension_infos[1]
          print(infoDict)
          filetypes.append(infoDict)
      infoDict={}
    rowFlag = not rowFlag


def writeData(obj):
  with open('./data/filetype.json', 'w') as fileObj:
    json.dump(obj, fileObj)

def readUrl():
  with open("./data/url_list.json", "r") as json_file:
    json_dict = json.load(json_file)
    return json_dict



if __name__=="__main__":
  urlList = readUrl()

  for i in range(len(urlList)):
    try:
      print('data collecting.....', i)
      getData(urlList[i])
      # 
    except err:
      print('gg 请重新开始')
      break
  
  writeData(filetypes)



