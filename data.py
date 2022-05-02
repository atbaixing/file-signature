# 处理重复数据
import json
def readData():
  # 通过第二个字段获取的数据有部分是重复的最终去除重复应该只有 518 条，当前 1872 条
  with open("./data/filetype.json", "r") as json_file:
    json_dict = json.load(json_file)
    return json_dict

def writeData(obj):
  with open('./data/suffix.json', 'w') as fileObj:
    json.dump(obj, fileObj)

if __name__=="__main__":
  data = readData()
  newDataArr = []

  for item in sorted(data, key=lambda x: x["extension_name"]):
    if item not in newDataArr:
      newDataArr.append(item)
      print(len(newDataArr))

  if(len(newDataArr)==518):
    writeData(newDataArr)
