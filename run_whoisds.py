from datetime import datetime
import pendulum

from corona import WhoisDs

save_path = './data/whoisds_files/{}/'.format(datetime.today().strftime('%Y-%m-%d'))

# Currently set to run for previous day (see .add(days=-1) below) to ensure availability
whoisds = WhoisDs(date=pendulum.now().add(days=-1), save_path=save_path).run()
