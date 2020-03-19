import os
from datetime import datetime, timedelta

from corona  import CZDS

d = datetime.today() - timedelta(days=1)
save_path = './data/zone_files/{}/'.format(d.strftime('%Y-%m-%d'))

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

czds = CZDS(USERNAME,PASSWORD, save_path=save_path).download()