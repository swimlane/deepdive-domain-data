from datetime import datetime, timedelta
import pendulum

from corona import WhoisDs

d = datetime.today() - timedelta(days=2)
save_path = './data/whoisds_files/{}/'.format(d.strftime('%Y-%m-%d'))

# Currently set to run for previous day (see .add(days=-1) below) to ensure availability
whoisds = WhoisDs(date=pendulum.now('UTC').add(days=-2), save_path=save_path).run()
