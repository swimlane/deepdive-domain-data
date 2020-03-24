import os, re, json
from datetime import datetime, timedelta

import pendulum
import confusables

from corona  import CZDS, WhoisDs, Corona

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

term_list = []

class RunDomainData(object):

    _date = datetime.today() - timedelta(days=2)
    _save_path = './data/{folder}/{date}/'

    def __run_czds(self):
        print('Running CZDS')
        czds_save_path = self._save_path.format(folder='zone_files',date=self._date.strftime('%Y-%m-%d'))
        czds = CZDS(USERNAME,PASSWORD, save_path=czds_save_path).download()
        print('Completed CZDS')

    def __run_whoids(self):
        print('Running WHOIDS')
        whoisds_save_path = self._save_path.format(folder='whoisds_files',date=self._date.strftime('%Y-%m-%d'))
        whoisds = WhoisDs(date=pendulum.now('UTC').add(days=-2), save_path=whoisds_save_path).run()
        print('Completed WHOISDS')

    def __run_corona(self):
        print('Running Corona')
        for item in ['corona','coronav','covid','pandemic','virus','vaccine']:
            term_list.append({
                'term': item,
                'value': re.compile(confusables.confusable_regex(item, include_character_padding=False), re.IGNORECASE | re.UNICODE)
            })
        corona = Corona().generate(term_list)
        print('Completed Corona')

    def __run_blacklist(self):
        print('Running Blacklist')
        json_save_path = self._save_path.format(folder='json_files',date=self._date.strftime('%Y-%m-%d'))
        master_blacklist_path = './data/blacklist/'
        blacklist_config = open('blacklist.config', 'r').read().split('\n')
        blacklist = []
        if os.path.exists(json_save_path):
            for json_file in os.listdir(json_save_path):
                if '_zone.json' in json_file:
                    if json_file.split('_')[0] in blacklist_config:
                        with open(os.path.join(json_save_path, json_file)) as f:
                            zone_dict = json.load(f)
                            for key,val in zone_dict.items():
                                for item in val:
                                    if 'domain' in item:
                                        if item['domain']:
                                            blacklist.append(item['domain'].strip())

            master_blacklist = list(set(blacklist))
            if not os.path.exists(master_blacklist_path):
                os.makedirs(master_blacklist_path)
            with open('{blacklist_path}master_blacklist.txt'.format(blacklist_path=master_blacklist_path), 'w+') as blacklist:
                blacklist.write("\n".join(master_blacklist))
        else:
            raise Exception('Unable to find json_files_path')
        print('Completed Blacklist')


    def run(self):
        #try:
        #    self.__run_czds()
        #except:
        #    raise Exception('Error running CZDS')

       # try:
       #     self.__run_whoids()
       # except:
        #    raise Exception('Error running WHOISDS')

       # try:
       #     self.__run_corona()
      #  except:
       #     raise Exception('Error running Corona')


        try:
            self.__run_blacklist()
        except:
            raise Exception('Error running Blacklist')
            
RunDomainData().run()