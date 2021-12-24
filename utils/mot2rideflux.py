from datetime import timedelta
import os
from tqdm import tqdm
import json
osp = os.path

# TODO Change Path
target = 'test'
# Dir to Test data  MSCOCO annotation format
test = f'datasets/rideflux/annotations/rideflux_coco_{target}.json'
# Result of Tracking data, MOT Format
result_data = 'datasets/bytetrack_results/test/real_result.json'
# Path to save final file
final = 'datasets/final'


class_mapping = {
    1: 'pedestrian',
    2: 'vehicle',
    3: 'bike',
}

test_anno = json.load(open(test, 'r'))

id2instance = {}


datas = json.load(open(result_data, 'r'))

for data in datas:
   if data in id2instance:
      id2instance[data].append(data)
   else:
      id2instance[data] = [data]

img_ids = sorted(list(id2instance.keys()))


for img_id in tqdm(img_ids):
# for img_id in img_ids:
    results = []
    for img in test_anno['images']:
        if img['file_name'] == img_id:
            anno = img
            break
    width = anno['width']
    height = anno['height']
    real_name = anno['file_name']
    frame_id = anno['frame_id']

    video_id = img_id.split('/')[0]
    os.makedirs(osp.join(final, video_id, 'json0'), exist_ok=True)

    json_file = {"annotations": [],
    "information": {"filename":img_id.split("/")[-1], "resolution":[width, height]}
    }
    
    track_datas = datas[img_id]
    for tdata in track_datas:
        sdata = tdata.split(",")
        tid = sdata[1]
        bbox = sdata[2:6]
        category = class_mapping[int(sdata[7])]
        new_dict = {"bbox":[int(float(bbox[0])), int(float(bbox[1])), int(float(bbox[2])+float(bbox[0])), int(float(bbox[3])+float(bbox[1]))],
        "attribute":{"track_id":int(tid)},
        "class":category
        
        }
        json_file['annotations'].append(new_dict)

    json.dump(json_file, open(osp.join(final, img_id.replace('jpg', 'json').replace('image0', 'json0')), 'w'))
