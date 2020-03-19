import os, json
from datetime import datetime

json_files_path = './data/json_files/{}/'.format(datetime.today().strftime('%Y-%m-%d'))
master_blacklist_path = './data/blacklist/'

blacklist = []
if os.path.exists(json_files_path):
    for json_file in os.listdir(json_files_path):
        if '_zone.json' in json_file:
            with open(os.path.join(json_files_path, json_file)) as f:
                zone_dict = json.load(f)
                for key,val in zone_dict.items():
                    for item in val:
                        if 'domain' in item:
                            if item['domain']:
                                blacklist.append(item['domain'])

    master_blacklist = list(set(blacklist))

    if not os.path.exists(master_blacklist_path):
        os.makedirs(master_blacklist_path)

    with open('{blacklist_path}master_blacklist.txt'.format(blacklist_path=master_blacklist_path), 'w+') as blacklist:
        blacklist.write("\n".join(master_blacklist))
else:
    raise Exception('Unable to find json_files_path')