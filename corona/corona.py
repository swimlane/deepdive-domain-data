import os, json, ast, re
import dns.resolver

class Corona(object):

    _zone_dict = {}
    _ip_dict = {}

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
        ip_dict = {}
        zone_dict = {}
        directory = directory.replace('json_files','zone_files')
        for zone in os.listdir(directory):
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
                                    if ip not in ip_dict:
                                        ip_dict[ip] = []
                                    ip_dict[ip].append(domain)
                            if zone.replace('.txt.gz','') not in zone_dict:
                                zone_dict[zone.replace('.txt.gz','')] = []
                            zone_dict[zone.replace('.txt.gz','')].append({
                                'domain': domain,
                                'ips': ips
                            })
            else:
                matches = [line for line in open('{}/{}'.format(directory, zone), "r") if re.match(term,line)]
                if matches:
                    for match in matches:
                        domain =  match.strip().split('\t')[0].rstrip('.')
                        ips = str(self.__get_dns_info(match.strip().split('\t')[0].rstrip('.'))).encode('utf-8')
                        ips = ast.literal_eval(ips.decode('utf-8'))
                        if isinstance(ips, list):
                            for ip in ips:
                                if ip not in ip_dict:
                                    ip_dict[ip] = []
                                ip_dict[ip].append(domain)
                        if zone.replace('.txt.gz','') not in zone_dict:
                            zone_dict[zone.replace('.txt.gz','')] = []
                        zone_dict[zone.replace('.txt.gz','')].append({
                            'domain': domain,
                            'ips': ips
                        })
        return ip_dict, zone_dict

    def __save_json(self, directory, term, type, data):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open('{directory}/{term}_{type}.json'.format(directory=directory,term=term, type=type), 'w+')
        f.write(json.dumps(data))
        f.close()

    def generate(self, term, value, directory, zone_file=None):
        ip_dict, zone_dict = self.__get_each_term(value, directory, zone_file=zone_file)
        self.__save_json(directory, term, 'ip', ip_dict)
        self.__save_json(directory, term, 'zone', zone_dict)