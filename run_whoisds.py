from datetime import datetime, timedelta
import pendulum
import os

from corona import WhoisDs

for dd in range(1, 23):
    d = datetime.today() - timedelta(days=dd)
    save_path = './data/whoisds_files/{}/'.format(d.strftime('%Y-%m-%d'))
    if os.path.isdir(save_path):
        print("Already Have WhoisDs data for {}".format(d.strftime('%Y-%m-%d')))
    else:
        print("Retrieving WhoisDs data for {}".format(d.strftime('%Y-%m-%d')))
        whoisds = WhoisDs(date=pendulum.now('UTC').add(days=-dd), save_path=save_path).run()
