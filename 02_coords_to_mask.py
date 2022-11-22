import glob
import threading

import json
import folium

import map_utils

token = "pk.eyJ1IjoiaGF1dHp5IiwiYSI6ImNsNXNzdGdidzA3cWUzaXQ4b25oMm5kcngifQ.YrWFM35R5Gyldf-I4nU4WQ"  # your mapbox token
TILE_URL = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)


def save_mask(dir):
    filepath = f"json/{dir}/*json"
    ind = 1
    for file_name in glob.glob(filepath):
        if True:
            print(file_name)
            with open(file_name, "r") as f:
                annotations = json.load(f)

            annotations.pop(0)
            lat_start = annotations[0][2]
            lon_start = annotations[0][1]

            positions = list()
            for point in annotations:
                positions.append((point[2], point[1]))

            mapObj = folium.Map(
                location=[lat_start, lon_start],
                zoom_start=17,
                attr='Mapbox',
                tiles=TILE_URL)

            map_name = "outputs/output_"+dir+".html"
            mapObj.save(map_name)

            map_utils.take_screenshot_of_map(map_name, "org_img_"+dir+".png")

            folium.PolyLine(positions, color='red', fill=True, fill_color="red",
                            fill_opacity=1).add_to(mapObj)

            mapObj.save(map_name)

            map_utils.take_screenshot_of_map(map_name, "field_img_"+dir+".png")

            map_utils.create_image_for_classification("org_img_"+dir+".png", "field_img_"+dir+".png",
                                                      dir+"/" + str(ind).zfill(2) + "_field.png")
        ind += 1


if __name__ == "__main__":
    #t1 = threading.Thread(target=save_mask, args=("obstbeaume",))
    #t2 = threading.Thread(target=save_mask, args=("dauerweide",))
    t3 = threading.Thread(target=save_mask, args=("wein",))
    #t4= threading.Thread(target=save_mask, args=("strauchbeeren",))
    #t5 = threading.Thread(target=save_mask, args=("hopfen",))

    #t2.start()
    # t2.start()
    t3.start()
    # t4.start()
    # t5.start()

    #t2.join()
    # t2.join()
    t3.join()
    # t4.join()
    # t5.join()
    print("DONE")
