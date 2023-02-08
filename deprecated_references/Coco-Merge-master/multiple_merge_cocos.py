from functions_for_merge_coco import *
import os
import glob
from tqdm import tqdm

def merge_multiple_cocos(path: str):
    '''
    :param path: Coco json's path
    :return: Merged coco json file
    '''
    project_files = (glob.glob(os.path.join(path, '*.json')))
    merged = {}
    merged['images'], merged['annotations'], merged['categories'] = [], [], []
    for index, path in enumerate(tqdm(project_files)):
        coco = config_reader(path)
        coco = get_the_unique_id_image(coco, 1000000000*(index+1))
        coco = get_unique_id_annotation(coco, 1000000000*(index+1))
        merged['images'] = coco['images'] + merged['images']
        merged['annotations'] = coco['annotations'] + merged['annotations']
        if index == (len(project_files)-1):
            merged['categories'] = coco['categories']
    return merged


# save_coco_file(merge_multiple_cocos('/home/izzet/Desktop/utility_turk'),'merged')

def merge_cocos_fetch_first_ten(path: str, step:int):
    '''
    :param path: Coco json's path
    :param step: decide to how many elements of coco json will be merged
    :return:
    '''
    project_files = (glob.glob(os.path.join(path, '*.json')))
    merged = {}
    merged['images'], merged['annotations'], merged['categories'] = [], [], []
    for index, path in enumerate(project_files):
        coco = config_reader(path)
        coco = get_the_unique_id_image(coco, 1000000000*(index+1))
        coco = get_unique_id_annotation(coco, 1000000000*(index+1))
        merged['images'] = coco['images'][:step] + merged['images']
        merged['annotations'] = coco['annotations'][:step] + merged['annotations']
        if index == (len(project_files)-1):
            merged['categories'] = coco['categories']
    return merged
