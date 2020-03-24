import os, ast, json
from datetime import datetime, timedelta

import dns.resolver


class Enrichment(object):

    _ip_dict = {}
    _zone_dict = {}

    def __get_dns_info(self, domain):
        return_list = []
        try:
            answers = dns.resolver.query(domain, 'A')
        except:
            return None
        for server in answers:
            return_list.append(server.to_text())
        return return_list


    def __generate_dicts(self):
         master_blacklist_file = './data/blacklist/master_blacklist.txt'
         if os.path.exists(master_blacklist_file):
            with open(master_blacklist_file) as fp:
                for cnt, line in enumerate(fp):
                    domain = line.strip()
                    dns_result = self.__get_dns_info(domain)
                    if dns_result:
                        ips = str(dns_result).encode('utf-8')
                        ips = ast.literal_eval(ips.decode('utf-8'))
                        if isinstance(ips, list):
                            for ip in ips:
                                if ip not in self._ip_dict:
                                    self._ip_dict[ip] = []
                                self._ip_dict[ip].append(domain)

                            if line not in self._zone_dict:
                                self._zone_dict[domain] = []
                            self._zone_dict[domain] = ips


    def __save_json(self, term_type, data):
        d = datetime.today() - timedelta(days=2)
        save_path = './data/json_files/{}'.format(d.strftime('%Y-%m-%d'))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        f = open('{directory}/{term}'.format(directory=save_path,term=term_type), 'w+')
        f.write(json.dumps(data))
        f.close()
    
    def run(self):
        self.__generate_dicts()
        self.__save_json('domains_by_ip.json', self._zone_dict)
        self.__save_json('ips_by_domain.json', self._ip_dict)