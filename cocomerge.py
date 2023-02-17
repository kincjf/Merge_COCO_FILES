import json
import argparse

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
    with open(opt, 'r', encoding='utf-8') as f:
        a = json.load(f) 
    # Merge Target First File Load
    with open(file1, 'r', encoding='utf-8') as f:
        coco_json_temp = json.load(f)
    # Merge Target Second File Load
    with open(file2, 'r', encoding='utf-8') as f:
        coco_json_temp1 = json.load(f)

    for i in [coco_json_temp,coco_json_temp1]:

        ch_cat_idx = {}
        ch_cat_name = {}
        ch_img_idx = {}
        ch_img_name = {}
        # Categories
        for j in i["categories"]:
            for l in a:
                if j["name"] in l["candidate_list"]:
                    ch_cat_idx[j["id"]] = l["merged_category_id"] # Changed Cat Idx List Up
                    j["id"] = l["merged_category_id"] # Change Cat Idx
                    j["name"] = l["merged_category_name"] # Change Cat Name
            for x in output_json['categories']:
                if j['name']==x["name"]:
                    flag_categories = False
                    break
            if flag_categories:
                output_json["categories"].append(j)
            flag_categories = True

        # images
        for j in i["images"]:
            ch_img_idx[j["id"]] = image_index # Changed Image Idx List Up
            j["id"] = image_index # Changed Image Idx
            output_json["images"].append(j)
            image_index += 1


        # annotations
        for j in i["annotations"]:
            # Require Check List
            # Apply Changed Cat, Img Idx
            # Chack List Up Value (Dict Type)
            # Cat Key = Category Name
            # Cat Value = Category Idx
            # Img Key = Img File name
            # Img Value = Img Idx
            j["id"] = ann_index
            j["image_id"] = ch_img_idx[j["image_id"]]
            j["category_id"] = ch_cat_idx[j["category_id"]]
            
            output_json["annotations"].append(j)
            ann_index += 1

    with open(output, 'w',encoding='utf-8') as f:
        json.dump(output_json,f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TEST ARGTEST")
    parser.add_argument('--file1', dest="file1", help='Filename (ex : ./coco_extract1.json)')
    parser.add_argument('--file2', dest="file2", help='Filename (ex : ./coco_extract2.json)')
    parser.add_argument('--opt', dest="opt", help='Filename (ex : ./merge_option.json)')
    parser.add_argument('--output', dest="output", help='Filename (ex : ./result.json)', default='result.json')
    # run('sample1Dataset.json','sample2Dataset.json','options.json','result.json')
    args = parser.parse_args()

    run(args.file1, args.file2, args.opt, args.output)
