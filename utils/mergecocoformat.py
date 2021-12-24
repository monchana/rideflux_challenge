import json
import os
# from tqdm import tqdm


# TODO Setup dataset directories
cityscapes_train_dir = 'datasets/cityscapes/annotations/instancesonly_filtered_gtFine_train.json'
cityscapes_val_dir = 'datasets/cityscapes/annotations/instancesonly_filtered_gtFine_val.json'

coco_train_dir = 'datasets/coco/annotations/instances_train2017.json'
coco_val_dir = 'datasets/coco/annotations/instances_val2017.json'

rideflux_train_dir = 'datasets/rideflux/annotation/rideflux_coco_train.json'
rideflux_val_dir = 'datasets/rideflux/annotation/rideflux_coco_val.json'


cityscapes_cat = [
    {'id': 1, 'name': 'person'},
    {'id': 2, 'name': 'rider'},
    {'id': 3, 'name': 'car'},
    {'id': 4, 'name': 'bicycle'},
    {'id': 5, 'name': 'bus'},
    {'id': 6, 'name': 'train'},
    {'id': 7, 'name': 'motorcycle'},
    {'id': 8, 'name': 'truck'}
    ]

cityscapes2rideflux = {
    1: 1,
    3: 2,
    4: 3,
    5: 2,
    7: 3,
    8: 2
}



coco_cat = [
    {'supercategory': 'person', 'id': 1, 'name': 'person'},
    {'supercategory': 'vehicle', 'id': 2, 'name': 'bicycle'},
    {'supercategory': 'vehicle', 'id': 3, 'name': 'car'},
    {'supercategory': 'vehicle', 'id': 4, 'name': 'motorcycle'},
    {'supercategory': 'vehicle', 'id': 6, 'name': 'bus'},
    {'supercategory': 'vehicle', 'id': 8, 'name': 'truck'},
]

coco2rideflux = {
    1: 1,
    2: 3,
    3: 2,
    4: 3,
    6: 2,
    8: 2
}



rideflux_cat = [
    {"id": 1, "name": "pedestrian"}, 
    {"id": 2, "name": "vehicle"}, 
    {"id": 3, "name": "bike"}
]

rideflux2rideflux = {
    0:1,
    1:2,
    2:3
}

cityscapes_train_data = json.load(open(cityscapes_train_dir, 'r'))
cityscapes_val_data = json.load(open(cityscapes_train_dir, 'r'))

coco_train_data = json.load(open(coco_train_dir, 'r'))
coco_val_data = json.load(open(coco_val_dir, 'r'))

rideflux_train_data = json.load(open(rideflux_train_dir, 'r'))
rideflux_val_data = json.load(open(rideflux_val_dir, 'r'))

total_val_data = {
    'images':[],
    'annotations':[],
    'categories':rideflux_cat,
}


total_train_data = {
    'images':[],
    'annotations':[],
    'categories':rideflux_cat,
}

last_val_img_id = 1
last_val_anno_id = 1

last_train_img_id = 1
last_train_anno_id = 1

# TODO : 어떤 소스를 쓰고 어떤 소스를 안 쓸지 결정해서 주석처리, 또는 삭제하면 됨 


# COCO VAL PART
image_ids = []
image_ids = sorted([x['id'] for x in coco_val_data['images']])
image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_val_img_id
    last_val_img_id += 1

new_imgs = []
for img in coco_val_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_imgs.append(new_img)

new_annos = []
for anno in coco_val_data['annotations']:
    if anno['category_id'] not in coco2rideflux.keys():
        continue
        
    new_anno = anno
    new_anno['category_id'] = coco2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_val_anno_id
    new_annos.append(new_anno)
    last_val_anno_id+=1

total_val_data['images'].extend(new_imgs)
total_val_data['annotations'].extend(new_annos)



# COCO TRAIN PART
image_ids = []
image_ids = sorted([x['id'] for x in coco_train_data['images']])
image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_train_img_id
    last_train_img_id += 1

new_imgs = []
for img in coco_train_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_imgs.append(new_img)

new_annos = []
for anno in coco_train_data['annotations']:
    if anno['category_id'] not in coco2rideflux.keys():
        continue
        
    new_anno = anno
    new_anno['category_id'] = coco2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_train_anno_id
    new_annos.append(new_anno)
    last_train_anno_id+=1

total_train_data['images'].extend(new_imgs)
total_train_data['annotations'].extend(new_annos)



# CityScapes VAL PART
image_ids = []
image_ids = sorted([x['id'] for x in cityscapes_val_data['images']])
image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_val_img_id
    last_val_img_id += 1

new_imgs = []
for img in cityscapes_val_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_img['file_name'] = img['file_name'].split('/')[-1]
    new_imgs.append(new_img)

new_annos = []
for anno in cityscapes_val_data['annotations']:
    if anno['category_id'] not in cityscapes2rideflux.keys():
        continue
        
    new_anno = anno
    new_anno['category_id'] = cityscapes2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_val_anno_id
    new_annos.append(new_anno)
    last_val_anno_id+=1

total_val_data['images'].extend(new_imgs)
total_val_data['annotations'].extend(new_annos)



# CityScapes Train PART
image_ids = []
image_ids = sorted([x['id'] for x in cityscapes_train_data['images']])
image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_train_img_id
    last_train_img_id += 1

new_imgs = []
for img in cityscapes_train_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_img['file_name'] = img['file_name'].split('/')[-1]
    new_imgs.append(new_img)

new_annos = []
for anno in cityscapes_train_data['annotations']:
    if anno['category_id'] not in cityscapes2rideflux.keys():
        continue
        
    new_anno = anno
    new_anno['category_id'] = cityscapes2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_train_anno_id
    new_annos.append(new_anno)
    last_train_anno_id+=1

total_train_data['images'].extend(new_imgs)
total_train_data['annotations'].extend(new_annos)


# Rideflux VAL PART
image_ids = []
image_ids = sorted([x['id'] for x in rideflux_val_data['images']])

image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_val_img_id
    last_val_img_id += 1

new_imgs = []
for img in rideflux_val_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_imgs.append(new_img)

new_annos = []
for anno in rideflux_val_data['annotations']:
    if anno['category_id'] not in rideflux2rideflux.keys():
        continue
    
    new_anno = anno
    new_anno['category_id'] = rideflux2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_val_anno_id
    new_annos.append(new_anno)
    last_val_anno_id+=1

total_val_data['images'].extend(new_imgs)
total_val_data['annotations'].extend(new_annos)

# Rideflux Train PART
image_ids = []
image_ids = sorted([x['id'] for x in rideflux_train_data['images']])
image_id_mapping = {}
for x in image_ids:
    image_id_mapping[x] = last_train_img_id
    last_train_img_id += 1

new_imgs = []
for img in rideflux_train_data['images']:
    new_img = img
    new_img['id'] = image_id_mapping[img['id']]
    new_imgs.append(new_img)

new_annos = []
for anno in rideflux_train_data['annotations']:
    if anno['category_id'] not in rideflux2rideflux.keys():
        continue
        
    new_anno = anno
    new_anno['category_id'] = rideflux2rideflux[anno['category_id']]
    new_anno['image_id'] = image_id_mapping[anno['image_id']]
    new_anno['id'] = last_train_anno_id
    new_annos.append(new_anno)
    last_train_anno_id+=1

total_train_data['images'].extend(new_imgs)
total_train_data['annotations'].extend(new_annos)

json.dump(total_val_data, open('total_val_data.json', 'w'))
json.dump(total_train_data, open('total_train_data.json', 'w'))