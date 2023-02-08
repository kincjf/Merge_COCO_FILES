import os
from addict import Dict
import json
import numpy as np
import pickle

def config_reader(path: str) -> Dict:
    with open(path) as f:
        cfg = json.load(f)
    return Dict(cfg)


def read_coco(path, filename):
    '''
    :param path: path of your json file
    :param filename: name of json file with '.json' extension.(example='train.json')
    :return:
    '''
    basePath = os.path.join(path)
    coco = config_reader(os.path.join(basePath, filename))
    return coco


def get_the_unique_id_image(coco, id=21):
    '''
    Start image id's some value
    for the  prevent id conflict
    :param coco: coco file type:dict
    :param id: starting value of ids. Default = 1000000
    :return: coco file type:dict
    '''
    id = id
    old_dic = {}
    for img in coco['images']:
        old_dic[id] = img['id']
        id += 1

    new_dict = dict([(value, key) for key, value in old_dic.items()])

    for img in coco['images']:
        img['id'] = new_dict.get(img['id'])

    for ann in coco['annotations']:
        ann['image_id'] = new_dict.get((ann["image_id"]))
    return coco


def get_the_unique_id_category(coco: Dict, id=400):
    '''
    category_id values will be start chosen value.
    :param coco: coco file type:Dict
    :param id: value of starting id
    :return: coco file type:Dictcd
    '''
    old_dic = {}

    for cat in coco['categories']:
        old_dic[id] = cat['id']
        id += 1
    new_dict = dict([(value, key) for key, value in old_dic.items()])

    for cat in coco['categories']:
        cat['id'] = new_dict.get(cat['id'])

    for ann in coco['annotations']:
        ann['category_id'] = new_dict.get((ann["category_id"]))

    return coco


def remove_some_category(coco: Dict, ids: list):
    '''
    Create a list that will be removed the
    categories.
    :param coco:  type:dict
    :param ids: chosen ids must in the list.
    :return:
    '''
    items = []
    ann_items = []

    for cat in coco['categories']:
        if not cat["id"] in ids:
            items.append(cat)

    for ann in coco['annotations']:
        if not ann["category_id"] in ids:
            ann_items.append(ann)

    coco['annotations'] = ann_items
    coco['categories'] = items
    return coco


def create_segmentation(coco: Dict):
    '''
    if boundry box array has a -1 value change to 1,
    if annotations has no segmentation info
     create segmentation array
    :param coco: type:Dict
    :return: new coco type:Dict
    '''
    for ann in coco['annotations']:
        [x1, y1, x2, y2] = [0 if x == 1 else x for x in ann['bbox']]
        ann['bbox'] = [x1, y1, x2, y2]
        ann['segmentation'] = [[x1, y1, x1, (y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
    return coco


def get_unique_id_annotation(coco, id=1000000):
    '''
    category_id values will be start chosen value.
    :param coco:
    :param id:
    :return:
    '''
    for ann in coco['annotations']:
        ann['id'] = id
        id += 1
    return coco


def check_the_unique(coco):
    '''
    check annotations id and  image id
    is unique. İf unique
    raturns True, otherwise False
    :param coco:
    :return:
    '''
    anno = []
    inami = []
    filename = []
    for ann in coco['annotations']:
        anno.append(ann['id'])
    for img in coco['images']:
        inami.append(img['id'])
        filename.append(img['file_name'])
    #    myset = set(filename)

    if (np.unique(anno).size == len(anno)) and (np.unique(inami).size == len(inami)):
        a = True
        print(len(anno), len(inami), len(filename))
        print(np.unique(anno).size, np.unique(inami).size)
    else:
        a = False
        print(len(anno), len(inami), len(filename))
        print(np.unique(anno).size, np.unique(inami).size)
    return a


def save_coco_file(coco, filename='sample'):
    with open(filename + '.json', "w") as fp:
        json.dump(coco, fp)


def duplicate_isim_cikar(coco):
    inami = []
    filename = []
    cikar_list = []
    items = []
    for img in coco['images']:
        inami.append(img['id'])
        filename.append(img['file_name'])
    uniq = set(filename)
    print(len(uniq), len(filename))
    seen = set()
    dupes = [x for x in filename if x in seen or seen.add(x)]
    for img in coco['images']:
        if img['file_name'] in dupes:
            cikar_list.append(img['id'])

    for img in coco['images']:
        if not img["id"] in cikar_list:
            items.append(img)
    coco['images'] = items
    print(len(cikar_list))
    return coco

def duplicate_image_id(coco):
    seen=set()
    seens=set()
    unique_values = [ann for ann in coco['annotations'] if ann['image_id'] in seen or seen.add(ann['image_id'])]
    unique_values2 = [img for img in coco['images'] if img['id'] in seens or seens.add(img['id'])]
    for ann in coco['annotations']:
        if ann['image_id'] in unique_values2:
            del ann

    print(unique_values2)
    coco['annotations'] = unique_values
    return coco

def cat_ids_update(coco,ids,new_id):
    for cat in coco['categories']:
        if cat["id"] in ids:
            cat['id'] = new_id

    for ann in coco['annotations']:
        if ann['category_id'] in ids:
            ann['category_id']=new_id
    return coco

def cat_name_update(coco,ids,new_name):
    for cat in coco['categories']:
        if cat["id"] in ids:
            cat['name'] = str(new_name)

    return coco
