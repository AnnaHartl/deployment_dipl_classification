import json
from typing import Any, List, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw
from rdp import rdp


def polygons_to_mask(
        polygons: List[List[Tuple[int, int]]],
        width: int = 600,
        height: int = 600,
) -> np.ndarray:
    mask = np.zeros((width, height))
    for idx, polygon in enumerate(reversed(polygons)):  # Latest annot likely worse annot
        if polygon.__len__() > 4:
            img = Image.new("L", (width, height), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=1, fill=0, width=3)
            mask += (idx + 1) * np.array(img)  # Add binary mask (0=background, (idx+1)=field)
            mask = np.clip(mask, a_min=0, a_max=(idx + 1))  # type: ignore
    return mask


def transform(values: List[Any]) -> List[List[Tuple[int, int]]]:
    boundaries = []
    for value in values:
        x = value["shape_attributes"]["all_points_x"]
        x += [x[-1]]
        y = value["shape_attributes"]["all_points_y"]
        y += [y[-1]]
        boundaries.append(list(zip(x, y)))
    return boundaries


def load_annotations(path: str, key) -> List[List[Tuple[int, int]]]:
    with open(path, "r") as f:
        annotations = json.load(f)
    annotation = annotations[key]
    # gibt nur die x und y werte jedes polygons in einer Liste zurück
    return transform(annotation["regions"])


def mask_to_polygons(
        mask: np.ndarray,
) -> List[List[Tuple[int, int]]]:
    """Transform a mask back to a polygon boundary."""
    polygons = []
    #jede Maske wird durchgegangen weil es können Mehrer Felder in einem Bild sein
    for v in sorted(set(np.unique(mask)) - {0}):
        # Extract polygon
        # Geht auf die Maske die gerade in der For schleife ist
        contours, _ = cv2.findContours(
            np.asarray(mask == v, dtype=np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        points = []
        for point in sorted(contours, key=lambda x: -len(x))[0]:  # If multiple (shouldn't be); use largest
            points.append([int(point[0][0]), int(point[0][1])])


        polygon = list([tuple(e) for e in rdp(points)])
        
        #Stellt sicher das der Anfang und das ende gleich sind
        if polygon[0] != polygon[-1]:
            polygon.append(polygon[0])
        polygons.append(polygon)

    return polygons
#
#
# def _is_line(data: Any) -> bool:
#     """Check if straight line."""
#     x, y = zip(*data)
#     assert len(x) == 3
#     for i in range(-2, 2 + 1):
#         if x[0] - i == x[1] == x[2] + i:
#             return True
#         if y[0] - i == y[1] == y[2] + i:
#             return True
#     return False
