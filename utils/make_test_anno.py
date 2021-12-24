import os
import cv2
from tqdm import tqdm
import json
osp = os.path

# TODO Change dirs
rideflux_root = 'datasets/rideflux'
test_dir = osp.join(rideflux_root, 'test')

datas =[]
target = 'test'
for root, dir, files in os.walk(test_dir):
    for file in files: 
        if 'jpg' in file:
            datas.append(file)

rideflux_classes = [
    {'id': 1, 'name': 'pedestrian'},
    {'id': 2, 'name': 'vehicle'},
    {'id': 3, 'name': 'bike'}
]

coco = {
    'images': [],
    'annotations' : [],
    'categories' : []
}

coco['categories'] = rideflux_classes


img_id = 1
prev_id = -1
next_id = 2

datas = sorted(datas)

img_mapping = {}

for i in tqdm(range(len(datas))):
    data = datas[i]
    img = cv2.imread(osp.join(test_dir, data.split('_')[0], 'image0', data))
    h, w, _ = img.shape
    coco['images'].append(
        {
            'file_name': osp.join(data.split('_')[0], 'image0', data),
            'width' : w,
            'height' : h,
            'id' : img_id,
            'frame_id' : int(data.split('_')[1].split('.')[0]),
            'video_id': int(data.split('_')[0]),
            'prev_image_id':prev_id,
            'next_image_id':next_id,
        }
    )

    img_mapping[img_id] = osp.join(data.split('_')[0], 'image0', data)
    prev_id = img_id
    img_id +=1 
    if i < len(datas) -1 :
        next_id = img_id + 1
    else:
        next_id = -1
    
json.dump(coco, open(osp.join(rideflux_root, 'annotations', f'rideflux_coco_{target}.json'), 'w'))
    