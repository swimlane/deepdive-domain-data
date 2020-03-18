import requests
import gzip
from datetime import datetime
import pendulum
from zipfile import ZipFile
import base64
import tldextract
from pathlib import Path


try:
    from StringIO import BytesIO  ## for Python 2
except ImportError:
    from io import BytesIO  ## for Python 3

class WhoisDs(object):
    def __init__(self, save_path=None, date=None):
        if date:
            self.date = date
        else:
            self.date = pendulum.now('UTC')
        self.save_path = save_path
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

    def latest(self):
        latest_list = []
        past = datetime.strftime(self.date, "%Y-%m-%d")
        print("Retrieving Domains Registered {}...".format(past))

        filename = "{}.zip".format(past)
        encoded_filename = base64.b64encode(filename.encode('utf-8'))

        response = requests.get('%s/%s/nrd' % ("https://whoisds.com//whois-database/newly-registered-domains", encoded_filename.decode('ascii')))

        try:
            with BytesIO(response.content) as zip_file:
                with ZipFile(zip_file) as zip_file:
                    for zip_info in zip_file.infolist():
                        with zip_file.open(zip_info) as ffile:
                            for line in ffile.readlines():
                                latest_list.append(line.decode('utf-8', errors='ignore').strip())
        except Exception as e:
            print("Unable to Unzip WhoisDs zone data -- data might not be generated yet.  {}".format(e))

        return latest_list

    def run(self):
        latest_list = self.latest()
        tld_dict = {}
        for domain in latest_list:
            try:
                t = tldextract.tldextract.extract(domain)
                if t.suffix not in tld_dict:
                    tld_dict[t.suffix] = []
                tld_dict[t.suffix].append(domain)
            except Exception as e:
                print(e)

        ret = {}
        for tld in tld_dict:
            ret[tld] = tld_dict[tld]
            filename = "{}.txt.gz".format(tld)
            text_string_list = '\n'.join(tld_dict[tld])
            text_string_bytes_object = BytesIO()
            text_string_bytes_object.write(text_string_list.encode('utf-8'))
            text_string_bytes_object.seek(0)
            with gzip.open('{0}{1}'.format(self.save_path, filename), 'wb') as f:
                f.write(text_string_bytes_object.read())

        return ret