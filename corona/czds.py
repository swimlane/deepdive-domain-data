import json
import requests
import sys, cgi, os, gzip
# import datetime

try:
    from StringIO import BytesIO ## for Python 2
except ImportError:
    from io import BytesIO ## for Python 3

class CZDS(object):

    BASE_URL = 'https://czds-api.icann.org'

    def __init__(self, username, password, save_path=None):
        self.save_path = save_path
        self.credential = {'username': username,
                    'password': password}
        self.token = self.authenticate()

    def authenticate(self):
        headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json'}

        url = 'https://account-api.icann.org/api/authenticate'

        response = requests.post(url, data=json.dumps(self.credential), headers=headers)

        status_code = response.status_code

        # Return the access_token on status code 200. Otherwise, terminate the program.
        if status_code == 200:
            access_token = response.json()['accessToken']
            return access_token
        elif status_code == 404:
            sys.stderr.write("Invalid url " + url)
            exit(1)
        elif status_code == 401:
            sys.stderr.write("Invalid username/password. Please reset your password via web")
            exit(1)
        elif status_code == 500:
            sys.stderr.write("Internal server error. Please try again later")
            exit(1)
        else:
            sys.stderr.write("Failed to authenticate with error code {1}".format(status_code))
            exit(1)

    def _get(self, url):
        bearer_headers = {'Content-Type': 'application/json',
                      'Accept': 'application/json',
                      'Authorization': 'Bearer {0}'.format(self.token)}

        response = requests.get(url, params=None, headers=bearer_headers, stream=True)
        return response

    def _get_zone_links(self):
        links_url = self.BASE_URL + "/czds/downloads/links"
        links_response = self._get(links_url)

        status_code = links_response.status_code

        if status_code == 200:
            zone_links = links_response.json()
            return zone_links
        elif status_code == 401:
            self.token = self.authenticate()
            self._get_zone_links()
        else:
            sys.stderr.write("Failed to get zone links from {0} with error code {1}\n".format(links_url, status_code))
            return None

    def _download_single_zone_file(self, url):
        response = self._get(url)
        status_code = response.status_code

        if status_code == 200:
            zone_name = url.rsplit('/', 1)[-1].rsplit('.')[-2]
            compressed_file = BytesIO(response.content)


            _,option = cgi.parse_header(response.headers['content-disposition'])
            filename = option['filename']

            if not filename:
                filename = zone_name + '.txt.gz'

            path_filename = "{}{}".format(self.save_path, filename)

            decompressed_file = gzip.GzipFile(fileobj=compressed_file, mode='rb')
            text_list = []
            for line in decompressed_file.readlines():
                domain = line.decode('utf-8').split('\t')[0].rstrip('.')
                text_list.append(domain)
            text_string_list = '\n'.join(list(set(text_list)))
            text_string_bytes_object = BytesIO()
            text_string_bytes_object.write(text_string_list.encode('utf-8'))
            text_string_bytes_object.seek(0)
            text_string_buf = text_string_bytes_object.read()

            gzip_object = gzip.compress(text_string_buf)
            gzip_size = gzip_object.__sizeof__()

            MAX_FILE_SIZE = 1024 * 1024 * 35
            if gzip_size >= MAX_FILE_SIZE:
                chapters = 0
                source_buf = gzip_object

                n = MAX_FILE_SIZE
                final = [source_buf[i * n:(i+1) * n] for i in range((len(source_buf) + n -1) // n)]  # list comprehension chunker

                for chunk in final:
                    chapters += 1
                    chapter_string = "{}".format(chapters)
                    chapter_string = chapter_string.zfill(2)
                    chapter_filename = "{}_{}{}".format(zone_name, chapter_string, '.txt.gz')
                    chapter_path_filename = "{}{}".format(self.save_path, chapter_filename)
                    with open(chapter_path_filename, 'wb+') as f:
                        f.write(chunk)
            else:
                with open(path_filename, 'wb+') as f:
                    f.write(gzip_object)

        elif status_code == 401:
            self.token = self.authenticate()
        elif status_code == 404:
            pass
        else:
            pass

    def download(self, zone_file_name=None):
        # The zone files will be saved in a sub-directory
        if self.save_path:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        # Download the zone files one by one
        for link in self._get_zone_links():
            if zone_file_name:
                if zone_file_name in link:
                    self._download_single_zone_file(link)
                else:
                    pass
            else:
                self._download_single_zone_file(link)

    def parse(self, content):
        return_list = []
        for line in content.splitlines():
            zone_list = {}
            record_data_list = []
            count = 1
            for item in line.split():
                if count == 1:
                    zone_list['dns_record'] = item
                elif count == 2:
                    zone_list['ttl'] = item
                elif count == 3:
                    zone_list['record_class'] = item
                elif count == 4:
                    zone_list['record_type'] = item
                else:
                    record_data_list.append(item)
                count += 1

            zone_list['record_data'] = ' '.join(record_data_list)
            return_list.append(zone_list)
        return return_list