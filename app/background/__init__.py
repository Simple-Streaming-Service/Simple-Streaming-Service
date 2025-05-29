from datetime import datetime
from dateutil.relativedelta import relativedelta

from app import scheduler
import app.services.maintenance as m

msg_archiving_delta = relativedelta(months=-1)
msg_deleting_delta = relativedelta(years=-1)
user_archiving_delta = relativedelta(years=-1)
user_deleting_delta = relativedelta(years=-5)

def maintenance_job():
    print('Maintenance time!', flush=True)
    print('Archived messages:',
          m.pack_old_messages(datetime.now() + msg_archiving_delta)
    )
    print('Deleted messages:',
          m.delete_old_messages(datetime.now() + msg_deleting_delta)
    )
    print('Archived users:',
          m.pack_old_users(datetime.now() + user_archiving_delta)
    )
    print('Deleted users:',
          m.delete_old_users(datetime.now() + user_deleting_delta)
    )
    print('Maintenance completed!', flush=True)


scheduler.add_job(maintenance_job, 'cron', hour=2, minute=0)
