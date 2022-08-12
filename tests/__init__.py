import logging
import datetime

start_dt = datetime.datetime.now()
start_str = start_dt.strftime('%Y%m%d-%H')
logging.basicConfig(filename=f"./log/perch-test-{start_str}.log",
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)
