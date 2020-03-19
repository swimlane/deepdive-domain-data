import os, json, ast, re
import gzip
from datetime import datetime
import dns.resolver

class Corona(object):

    zone_dict = {}
    ip_dict = {}
    _folder_list = ['zone_files','whoisds_files']

    def __get_dns_info(self, domain):
        return_list = []
        try:
            answers = dns.resolver.query(domain,'A')
        except:
            return None
        for server in answers:
            return_list.append(server.to_text())
        return return_list

    def __get_each_term(self, term, directory, zone_file=None):
        #directory = directory.replace('json_files','zone_files')
        for zone in os.listdir(directory):
            
            #decompressed_file = gzip.open(os.path.join(directory,zone))
            if zone_file:
                if zone_file in zone:
                    matches = [line for line in open('{}/{}'.format(directory, zone), "r") if re.match(term,line)]
                    if matches:
                        for match in matches:
                            domain =  match.strip().split('\t')[0].rstrip('.')
                            ips = str(self.__get_dns_info(match.strip().split('\t')[0].rstrip('.'))).encode('utf-8')
                            ips = ast.literal_eval(ips.decode('utf-8'))
                            if isinstance(ips, list):
                                for ip in ips:
                                    if ip not in self.ip_dict:
                                        self.ip_dict[ip] = []
                                    self.ip_dict[ip].append(domain)
                            if zone.replace('.txt.gz','') not in self.zone_dict:
                                self.zone_dict[zone.replace('.txt.gz','')] = []
                            self.zone_dict[zone.replace('.txt.gz','')].append({
                                'domain': domain,
                                'ips': ips
                            })
            else:
                try:
                    with gzip.open('{}/{}'.format(directory,zone),'rt') as f:
                        for line in f:
                            if re.match(term, line):
                                print('got line', line)
                
                                ips = str(self.__get_dns_info(line)).encode('utf-8')
                                ips = ast.literal_eval(ips.decode('utf-8'))
                                if isinstance(ips, list):
                                    for ip in ips:
                                        if ip not in self.ip_dict:
                                            self.ip_dict[ip] = []
                                        self.ip_dict[ip].append(line)
                                if zone.replace('.txt.gz','') not in self.zone_dict:
                                    self.zone_dict[zone.replace('.txt.gz','')] = []
                                self.zone_dict[zone.replace('.txt.gz','')].append({
                                    'domain': line,
                                    'ips': ips
                                })
                except:
                    pass

    def __save_json(self, directory, term, type, data):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open('{directory}/{term}_{type}.json'.format(directory=directory,term=term, type=type), 'w+')
        f.write(json.dumps(data))
        f.close()

    def generate(self, term, value, zone_file=None):
        date = datetime.today().strftime('%Y-%m-%d')
        for folder in self._folder_list:
            directory = './data/{folder}/{date}/'.format(folder=folder, date=date)
            self.__get_each_term(value, directory, zone_file=zone_file)
        self.__save_json('./data/json_files/{}'.format(date), term, 'ip', self.ip_dict)
        self.__save_json('./data/json_files/{}'.format(date), term, 'zone', self.zone_dict)