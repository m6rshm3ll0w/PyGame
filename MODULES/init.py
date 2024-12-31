import json

with open('./DATA/settings.json', "r", encoding="UTF-8") as json_data:
    CONFIG = json.load(json_data)

