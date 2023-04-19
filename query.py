import pathlib
from pathlib import Path
import os
import json
import random

data_dir = '/share-4dgt/chengqi.li/ShapeNetCore.v2'
taxonomy_json = os.path.join(data_dir, 'taxonomy.json')
with open(taxonomy_json, 'rb') as f:
    taxonomy = json.load(f)


def query_objs(obj_id: str):

    for dir_name in os.listdir(data_dir):
        cls = [synset for synset in taxonomy if synset['synsetId'] == dir_name]
        cls = cls[0] if len(cls) == 1 else None
        if cls == None:
            continue
        # print(cls['name'], cls['synsetId'])

        all_objs = os.listdir(os.path.join(data_dir, dir_name))
        query_list = [x for x in all_objs if obj_id in x]
        if len(query_list) > 0:
            print(cls['name'], cls['synsetId'], 'obj_id:', query_list)
            return query_list


def gen_train_list(dir: Path, id="02958343"):
    data_dir = f'/share-4dgt/chengqi.li/SdfSamples/ShapeNetV2/{id}'
    all_objs = []
    for dir_name in os.listdir(data_dir):
        all_objs.append(dir_name.replace('.npz', ''))

    random.shuffle(all_objs)
    train_list = all_objs[:int(len(all_objs) * 0.8)]
    test_list = all_objs[int(len(all_objs) * 0.8):]
    train_json = {
        "ShapeNetV2": {
            id: train_list
        }
    }
    with open(dir/"train.json", 'w') as f:
        json.dump(train_json, f, indent=4)

    train_json = {
        "ShapeNetV2": {
            id: test_list
        }
    }
    with open(dir/"test.json", 'w') as f:
        json.dump(train_json, f, indent=4)


if __name__ == "__main__":
    query_objs('7079f58ade8d5a774a206e129eab0d56')
    # gen_train_list(dir=Path('/home/chengqi.li/DeepSDF/examples/splits'))

