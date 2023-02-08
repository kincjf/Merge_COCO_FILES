import json
import os

#파일 리스트 가져오는 코드
file_list = os.listdir('./coco_extract_folder')

#json 만 가져오기
json_list = []
for i in file_list:
    if ".json" in i:
        json_list.append(i)

#json list
output_json = {
  "licenses": [{ "name": "", "id": 0, "url": "" }],
  "info": {
    "contributor": "",
    "date_created": "",
    "description": "",
    "url": "",
    "version": "",
    "year": ""
  },
  "categories": [
    
  ],
  "images": [
    
  ],
  "annotations": [
    
  ]
}

# 가져온 json 파일 리스트를 하나씩 불러서 카테고리, 이미지 ,언노테이션등 을 비교 하는 코드 작성.

# 예를 들어

# 비슷한 단어를 모아놓은 배열 a가 있음

a = ['teeth', 'oral','mouse','dental']

image_index = 1
ch_image_key_to_index = {}
ol_image_id_to_newid = {}

ann_index = 1
# ann_key_to_index = {}
tt = {}
# trretret

flag_categories = True

for i in json_list:
    with open(f'./coco_extract_folder/{i}', 'r', encoding='utf-8') as f:
        coco_json_temp = json.load(f)
    
    for j in coco_json_temp['categories']:
       if j['name'] in a:
        j['id']=1
        j['name']='teeth'
        for x in output_json['categories']:
            if j['name']==x["name"]:
                flag_categories = False
            
        if flag_categories:
            output_json['categories'].append(j)
        flag_categories = True

    for j in coco_json_temp['images']:
        j['id'] = image_index
        image_index += 1
        if not j['file_name'] in ch_image_key_to_index.keys():
            # 변경되는 image index 값을 만듬
            ch_image_key_to_index[j['file_name']] = image_index
            ol_image_id_to_newid[j['id']] = j['file_name']
        output_json['images'].append(j)
    
    for j in coco_json_temp['annotations']:
        j["image_id"] = ch_image_key_to_index[ol_image_id_to_newid[j['image_id']]]
        output_json["annotations"].append(j)
    
with open("output.json", 'w') as f:
        json.dump(output_json,f)
