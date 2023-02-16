# Merge_COCO_FILES

Simple yet fully working tool

## Requirments
`python==3.x`

## Installation
```
Simply:
1- git clone https://github.com/mohamadmansourX/Merge_COCO_FILES.git
2- cd Merge_COCO_FILES
```

## COCO Files Merge Usage
```
python merge.py Json1.json Json2.json OUTPU_JSON.json
```

Json1 and Json2 are the two COCO files to be merged.

OUTPU_JSON is the output file for the combined results

<br>

**Note:**

The script will do the following checks as well:
1. Duplicate filenames checks (to count if the same image has two annotations)
2. Categories checks (Both files should have same categegories (name, id))

The reason I didn't mix categories, incase they are different, is to help annotators identifying any change in there categories. 
I believe this will be helpful incase of annotating a dataset as batches or splitting the annotation on members. Any change in ids caused by software being used or human mistake will be directly identified.
  

Example of Dog category existing in file 2 but not file 1
  
<code>AssertionError: Category name: Dog in file 2 does not exist in file 1</code>


Example of Cat category existing in both files but with different ids:

<code>AssertionError: Category name: Cat, id: 1 in file 1 and 2 in file 2</code>
<br>

## COCO File Class Edit Usage

```
python INPUT_JSON.json OUTPU_JSON.json Label1 Label2...
```

*Note: the script will do the necessary checks as well (duplicate filenames, ....)*


## references
pytest example코드 참고1: https://github.com/kennethreitz/requests/blob/master/tests/test_help.py

https://www.google.com/search?q=pytest+vs+unittest


https://www.google.com/search?q=coco+data+json+image+label+split

https://github.com/akarazniewicz/cocosplit


https://docs.voxel51.com/api/fiftyone.core.dataset.html?highlight=merge_samples#fiftyone.core.dataset.Dataset.merge_samples   \
https://docs.voxel51.com/recipes/merge_datasets.html   \
fiftyone에 카테고리id라벨 merge기능이 있는지 찾아봤는데, Func을 몇개 이용해서 구현할수는 있으나, 한번설정으로 실행되는 func는 없음 


### 구현기능 test용 샘플데이터세트 준비-다운로드 방법자료
https://cocodataset.org/#download

https://stackoverflow.com/questions/51100191/how-can-i-download-a-specific-part-of-coco-dataset

https://docs.voxel51.com/tutorials/open_images.html

https://docs.voxel51.com/user_guide/dataset_zoo/datasets.html#dataset-zoo-coco-2017

https://cocodataset.org/#explore