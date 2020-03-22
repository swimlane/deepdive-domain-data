import os, json, ast, re
import gzip
from datetime import datetime, timedelta
import dns.resolver
try:
    from StringIO import BytesIO ## for Python 2
except ImportError:
    from io import BytesIO ## for Python 3


class Corona(object):

    zone_dict = {}
    ip_dict = {}
    _czds_folder_list = ['zone_files']
    _whoisds_folder_list = ['whoisds_files']

    def __get_dns_info(self, domain):
        return_list = []
        try:
            answers = dns.resolver.query(domain, 'A')
        except:
            return None
        for server in answers:
            return_list.append(server.to_text())
        return return_list

    def __get_each_term(self, term_list, directory, zone_file=None):
        chunked_files = {}
        try:
            zones = os.listdir(directory)
            zones = sorted(zones)
        except:
            print(os.listdir('./data/zone_files/'))
            print(os.listdir('./data/whoisds_files/'))
            raise Exception('Unable to find appropriate source files.')
        for zone in zones:
            if '_' in zone:
                key = zone.split('_')[0]
                if key not in chunked_files:
                    chunked_files[key] = BytesIO()
                with open('{}/{}'.format(directory, zone), 'rb') as f:
                    chunked_files[key].write(f.read())
            else:
                try:
                    with gzip.open('{}/{}'.format(directory,zone), 'rt') as f:
                        for line in f:
                            for term in term_list:
                                if term['value'].search(line):
                                    ips = str(self.__get_dns_info(line.strip())).encode('utf-8')
                                    ips = ast.literal_eval(ips.decode('utf-8'))
                                    if isinstance(ips, list):
                                        for ip in ips:
                                            if term['term'] not in self.ip_dict:
                                                self.ip_dict[term['term']] = {}
                                            if ip not in  self.ip_dict[term['term']]:
                                                self.ip_dict[term['term']][ip] = []
                                            self.ip_dict[term['term']][ip].append(line)

                                    if term['term'] not in self.zone_dict:
                                        self.zone_dict[term['term']] ={}
                        
                                    if zone.replace('.txt.gz','') not in self.zone_dict[term['term']]:
                                        self.zone_dict[term['term']][zone.replace('.txt.gz','')] = []
                                    self.zone_dict[term['term']][zone.replace('.txt.gz','')].append({
                                        'domain': line,
                                        'ips': ips
                                    })
                except:
                    pass

        if len(chunked_files) > 0:
            for key in chunked_files:
                chunked_files[key].seek(0)
                with gzip.open(chunked_files[key], 'rt') as f:
                    for line in f.readlines():
                        line = line.strip()
                        for term in term_list:
                            if term['value'].search(line):
                                ips = str(self.__get_dns_info(line)).encode('utf-8')
                                ips = ast.literal_eval(ips.decode('utf-8'))
                                if isinstance(ips, list):
                                    for ip in ips:
                                        if term['term'] not in self.ip_dict:
                                            self.ip_dict[term['term']] = {}
                                        if ip not in  self.ip_dict[term['term']]:
                                            self.ip_dict[term['term']][ip] = []
                                        self.ip_dict[term['term']][ip].append(line)

                                if term['term'] not in self.zone_dict:
                                    self.zone_dict[term['term']] ={}
                    
                                if zone.replace('.txt.gz','') not in self.zone_dict[term['term']]:
                                    self.zone_dict[term['term']][zone.replace('.txt.gz','')] = []
                                self.zone_dict[term['term']][zone.replace('.txt.gz','')].append({
                                    'domain': line,
                                    'ips': ips
                                })
                                
                                

    def __save_json(self, directory, type, data):
        if not os.path.exists(directory):
            os.makedirs(directory)
        for key,val in data.items():
            f = open('{directory}/{term}_{type}.json'.format(directory=directory,term=key, type=type), 'w+')
            f.write(json.dumps(val))
            f.close()

    def generate(self, term_list):
        d = datetime.today() - timedelta(days=2)
        # save_path = './data/zone_files/{}/'.format(d.strftime('%Y-%m-%d'))
        date = d.strftime('%Y-%m-%d')
        for folder in self._czds_folder_list:  # for full zone transfer files (i.e. czds)
            directory = './data/{folder}/{date}/'.format(folder=folder, date=date)
            self.__get_each_term(term_list, directory)
        for folder in self._whoisds_folder_list:  # for daily new files (i.e. whoisds)
            directory_names = []
            whoisds_directory = './data/{folder}/'.format(folder=folder)
            for root, d_names, f_names in os.walk(whoisds_directory):
                for d in d_names:
                    directory_names.append(os.path.join(root, d))
            for directory in directory_names:
                self.__get_each_term(term_list, directory)

        # self.__get_each_term(term_list)
        self.__save_json('./data/json_files/{}'.format(date), 'ip', self.ip_dict)
        self.__save_json('./data/json_files/{}'.format(date), 'zone', self.zone_dict)