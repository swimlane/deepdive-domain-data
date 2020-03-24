import os, re, json
from datetime import datetime, timedelta
import confusables

import pendulum

from corona  import CZDS, WhoisDs, Corona

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

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

    def __run_blacklist(self):
        print('Running Blacklist')
        blacklist_config = open('blacklist.config', 'r').read().split('\n')
        blacklist_terms = []
        for item in blacklist_config:
            if len(item.strip()) > 0:
                blacklist_terms.append(item.strip())
        term_list = []
        for item in blacklist_terms:
            term_list.append({
                'term': item,
                'value': re.compile(confusables.confusable_regex(item, include_character_padding=False), re.IGNORECASE | re.UNICODE)
            })
        corona = Corona().generate(term_list)
        print('Completed Blacklist')

    def run(self):
        try:
           self.__run_czds()
        except:
            raise Exception('Error running CZDS')

        try:
            self.__run_whoids()
        except:
            raise Exception('Error running WHOISDS')

        try:
            self.__run_blacklist()
        except:
            raise Exception('Error running Blacklist')
            
RunDomainData().run()