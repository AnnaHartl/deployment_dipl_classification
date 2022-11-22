import fiona
import requests

import config_json_files as conf
import json
import os

URL = 'https://mygeodata.cloud/data/cs2cs'
INCRS = "+proj=lcc +lat_1=49 +lat_2=46 +lat_0=47.5 +lon_0=13.33333333333333 +x_0=400000 +y_0=400000 +datum=hermannskogel +units=m +no_defs"
OUTCRS = "+proj=longlat +datum=WGS84 +no_defs"


def create_dirextories(dir_names):
    try:
        path = os.getcwd()
        print(path)
        #os.mkdir(path + "/csv")
        os.mkdir(path + "/json")
        os.mkdir(path + "/outputs")
        for name in dir_names:
            os.mkdir(path + "/json/" + name.lower())
            os.mkdir(path + "/outputs/" + name.lower())
    except FileExistsError:
        print("Ordner schon vorhanden")


def convert_to_lat_long(coordinates, type):
    result = list()
    result.append(type)
    payload = ''
    for coordinate in coordinates:
        payload += f'{coordinate[0]} {coordinate[1]}%n\n'

    post = requests.post(url=URL,
                         data={'coords': payload, 'incrs': INCRS, 'outcrs': OUTCRS, 'addinput': 'false',
                               'switch': 'false'},
                         headers={})
    data = post.json()
    data = data['data']
    #print(data)
    lines = data.split('\n')
    i = 0
    for line in lines:
        if len(line) <= 0:
            continue
        parts = line.split(';')
        result.append((i, float(parts[0]), float(parts[1])))
        i += 1
    return result


def create_json_files():
    with fiona.open('dist/INSPIRE_SCHLAEGE_2022_POLYGON.gpkg') as layer:
        for feature in layer:
            # print(feature)
            id = feature['id']
            properties = feature['properties']
            field_type = properties['SNAR_BEZEICHNUNG']
            geometry = feature['geometry']
            coordinates = geometry['coordinates']
            for i in range(conf.CLASSES.__len__()):
                if field_type in conf.CLASSES[i]["name"] and conf.CLASSES[i]["count"] < conf.MAX_COUNT:
                    converted_coords = convert_to_lat_long(coordinates[0], field_type)
                    with open(conf.CLASSES[i]["json_dir"] + id + ".json", "w") as f:
                        json.dump(converted_coords, f)
                    conf.CLASSES[i]["count"] += 1
                print(conf.CLASSES[i]["new_name"]+": "+str(conf.CLASSES[i]["count"]), end="; ")
            print()

            # if conf.CLASSES[4]["count"] < conf.MAX_COUNT and int(id) % conf.PERIOD == 0 and field_type not in \
            #         conf.CLASSES[4]["name"]:
            #     converted_coords = convert_to_lat_long(coordinates[0], "ANDERES")
            #     with open(conf.CLASSES[4]["json_dir"] + id + ".json", "w") as f:
            #         json.dump(converted_coords, f)
            #     conf.CLASSES[4]["count"] += 1

            print(id, field_type)

            if conf.CLASSES[0]["count"] == conf.MAX_COUNT and \
                    conf.CLASSES[1]["count"] == conf.MAX_COUNT and \
                    conf.CLASSES[2]["count"] == conf.MAX_COUNT and \
                    conf.CLASSES[3]["count"] == conf.MAX_COUNT and \
                    conf.CLASSES[4]["count"] == conf.MAX_COUNT:
                break
        print("done")


if __name__ == "__main__":
    create_dirextories(conf.NEW_CLASS_NAMES)
    create_json_files()