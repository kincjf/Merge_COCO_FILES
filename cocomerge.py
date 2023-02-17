import json
import argparse

#json list
output_json = {
   "licenses": [],
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


tt = {}

def run(file1,file2,opt,output):
    """_summary_

    Args:
        file1 (_type_): _description_
        file2 (_type_): _description_
        opt (_type_): _description_
        output (_type_): _description_
    """
    image_index = 1
    ann_index = 1
    flag_categories = True
    # Option File load
    with open(opt, 'r', encoding='utf-8') as opt_file:
        options = json.load(opt_file) 
    # Merge Target First File Load
    with open(file1, 'r', encoding='utf-8') as file1:
        coco_json_temp1 = json.load(file1)
    # Merge Target Second File Load
    with open(file2, 'r', encoding='utf-8') as file2:
        coco_json_temp2 = json.load(file2)

    output_json["info"] = coco_json_temp1["info"]
    output_json["licenses"] = coco_json_temp1["licenses"]
    for i in [coco_json_temp1, coco_json_temp2]:

        ch_cat_idx = {}
        ch_cat_name = {}
        ch_img_idx = {}
        ch_img_name = {}
        # Categories
        # for j in i["categories"]:
        for category in i["categories"]:
            for option in options:
                if category["name"] in option["candidate_list"]:
                    ch_cat_idx[category["id"]] = option["merged_category_id"] # Changed Cat Idx List Up
                    category["id"] = option["merged_category_id"] # Change Cat Idx
                    category["name"] = option["merged_category_name"] # Change Cat Name
            for x in output_json['categories']:
                if category['name']==x["name"]:
                    flag_categories = False
                    break
            if flag_categories:
                output_json["categories"].append(category)
            flag_categories = True

        # images
        # segmentation 같이 dataset 특성별로 존재할수도 있고 존재하지 않을수도 있는 값들은, append 같이 그냥 붙여넣는다
        for image in i["images"]:
            ch_img_idx[image["id"]] = image_index # Changed Image Idx List Up
            image["id"] = image_index # Changed Image Idx
            output_json["images"].append(image)
            image_index += 1


        # annotations
        # 바꿀변수값[id, image_id, category_id]을 제외하고는 나머지는 순차적으로 넣음
        # segmentation 같이 dataset 특성별로 존재할수도 있고 존재하지 않을수도 있는 값들은, append 같이 그냥 붙여넣는다
        for annotation in i["annotations"]:
            # Require Check List
            # Apply Changed Cat, Img Idx
            # Chack List Up Value (Dict Type)
            # Cat Key = Category Name
            # Cat Value = Category Idx
            # Img Key = Img File name
            # Img Value = Img Idx
            annotation["id"] = ann_index
            annotation["image_id"] = ch_img_idx[annotation["image_id"]]
            annotation["category_id"] = ch_cat_idx[annotation["category_id"]]
            
            output_json["annotations"].append(annotation)
            ann_index += 1

    with open(output, 'w',encoding='utf-8') as f:
        json.dump(output_json,f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TEST ARGTEST")
    parser.add_argument('--file1', dest="file1", help='Filename (ex : ./coco_extract1.json)')
    parser.add_argument('--file2', dest="file2", help='Filename (ex : ./coco_extract2.json)')
    parser.add_argument('--opt', dest="opt", help='Filename (ex : ./merge_option.json)')

    # --output 안적을 경우, default='instances_.json' 으로 출력됨
    parser.add_argument('--output', dest="output", help='Filename (ex : ./result.json)', default='instances_.json')
    # run('sample1Dataset.json','sample2Dataset.json','options.json','result.json')
    args = parser.parse_args()

    run(args.file1, args.file2, args.opt, args.output)
