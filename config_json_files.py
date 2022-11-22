MAX_COUNT = 500
PERIOD = 2
CLASS_NAMES = ["WEIN","DAUERWEIDE", "TAFELBIRNEN", "TAFELÄPFEL", "MARILLEN", "PFIRSICHE", "ZWETSCHKEN", "PFLAUMEN", "HOPFEN"]
NEW_CLASS_NAMES = ["WEIN", "DAUERWEIDE", "HOPFEN",] #"OBSTBEAUME",  "STRAUCHBEEREN"
CLASSES = [
    {
        "name": "WEIN",
        "new_name": "WEIN",
        "json_dir": "json/wein/",
        "count": 0
    },
    {
        "name": "DAUERWEIDE",
        "new_name": "DAUERWEIDE",
        "json_dir": "json/dauerweide/",
        "count": 0
    },
#     {
#         "name": ["TAFELBIRNEN", "TAFELÄPFEL", "MARILLEN", "PFIRSICHE", "ZWETSCHKEN", "PFLAUMEN"],
#         "new_name": "OBSTBEAUME",
#         "json_dir": "json/obstbeaume/",
#         "count": 0
#     },
# {
#         "name": "STRAUCHBEEREN",
#         "new_name": "STRAUCHBEEREN",
#         "json_dir": "json/strauchbeeren/",
#         "count": 0
#     },
    {
        "name": "HOPFEN",
        "new_name": "HOPFEN",
        "json_dir": "json/hopfen/",
        "count": 0
    },
    # {
    #     "name": CLASS_NAMES,
    #     "newName": "OTHER",
    #     "json_dir": "json/other/",
    #     "count": 0
    # }
]
