import json
import os
osp = os.path

# TODO Change directory
rideflux_root = 'datasets/rideflux'

target = 'test'
coco = {
    'images': [],
    'annotations' : [],
    'categories' : []
}

# with open(f'rideflux_{target}.txt', 'r') as openfile:
#     datas = [x.replace('\n', '') for x in openfile.readlines()]

datas = []

for root, dir, files in os.walk(osp.join(rideflux_root, target)):
    for file in files: 
        if 'jpg' in file:
            datas.append(file)

datas=sorted(datas)
# special category for rideflux
rideflux_classes = [
    {'id': 1, 'name': 'pedestrian'},
    {'id': 2, 'name': 'vehicle'},
    {'id': 3, 'name': 'bike'}
]

class_mapping = {
    'pedestrian': 1,
    'vehicle': 2,
    'bike': 3,
}

coco['categories'] = rideflux_classes

ann_id = 1
img_id = 1
prev_id = -1
next_id = 2
for i in range(len(datas)):
    data = datas[i]
    json_name = data.replace('jpg', 'json')
    # img_id = ''.join(json_name.split('.')[0].split('_')) # 10019000 format
    # as datas are sampled from validation
    json_data = json.load(open(osp.join(rideflux_root, target, json_name.split('_')[0], 'json0', json_name)))
    
    coco['images'].append(
        {
            'file_name': osp.join(data.split('_')[0], 'image0', data),
            'width' : json_data['information']['resolution'][0],
            'height' : json_data['information']['resolution'][1],
            'id' : img_id,
            'frame_id' : int(data.split('_')[1].split('.')[0]),
            'video_id': int(data.split('_')[0]),
            'prev_image_id':prev_id,
            'next_image_id':next_id,
        }
    )
    for instance in json_data['annotations']:
        bbox = instance['bbox']
        coco['annotations'].append(
            {
                'image_id': img_id,
                'iscrowd': 0,
                # 'track_id': json_name.split('.')[0].split('_')[0] + '_' + str(instance['attribute']['track_id']),
                'track_id': instance['attribute']['track_id'],
                'bbox': [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]],
                'area': (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]),
                'category_id': class_mapping[instance['class']],
                'id': ann_id,
                # 'id': img_id + '_' + str(instance['attribute']['track_id']),
            }
        )
        ann_id += 1
    prev_id = img_id
    img_id +=1 
    if i < len(datas) -1 :
        next_id = img_id + 1
    else:
        next_id = -1

os.makedirs(osp.join(rideflux_root, 'annotations'), exist_ok=True)
json.dump(coco, open(osp.join(rideflux_root, 'annotations', f'rideflux_coco_{target}.json'), 'w'))
    
