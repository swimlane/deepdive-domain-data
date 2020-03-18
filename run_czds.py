import os
from datetime import datetime

from corona  import CZDS

save_path = './data/zone_files/{}/'.format(datetime.today().strftime('%Y-%m-%d'))

czds = CZDS(os.environ['USERNAME'],os.environ['PASSWORD'], save_path=save_path).download()