import cv2
import os
import json
from tqdm import tqdm
osp = os.path

# TODO Change target and directories
target = 'val'
picroot = 'datasets/rideflux'
jsonroot = 'datasets/rideflux_archive'

count = 0
for pic in tqdm(os.listdir(osp.join(picroot, target))):
    changed = 0
    first_name = pic.split('_')[0]
    json_name = pic.replace('jpg', 'json')

    img = cv2.imread(osp.join(picroot, target, pic))
    h, w, _ = img.shape

    data = json.load(open(osp.join(jsonroot, target, first_name, 'json0', json_name), 'r'))
    jw, jh = data['information']['resolution']

    if jw != w or jh!= h :
        count +=1
        changed = 1

    if jw != w:
        data['information']['resolution'][0] = w
        changed = 1

    if jh != h:
        data['information']['resolution'][1] = h
        changed = 1

    if changed:
        print(pic)
        json.dump(data, open(osp.join(jsonroot, target, first_name, 'json0', json_name), 'w'))

print('Changed : ' , count)