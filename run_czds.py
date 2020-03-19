import os
from datetime import datetime

from corona  import CZDS

save_path = './data/zone_files/{}/'.format(datetime.today().strftime('%Y-%m-%d'))

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

czds = CZDS(USERNAME,PASSWORD, save_path=save_path).download()