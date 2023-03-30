from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

from Donations.schema import (
    delete_expired_blood,
    delete_expired_plasma,
    delete_expired_platelets,
    donation_expired
)

delete_expired_blood_task = app.task(delete_expired_blood)
delete_expired_platelets_task = app.task(delete_expired_platelets)
delete_expired_plasma_task = app.task(delete_expired_plasma)
donation_expired_task = app.task(donation_expired)

@app.task
def destroy_expired_donations_task():
    donation_expired_task()
    delete_expired_blood_task()
    delete_expired_plasma_task()
    delete_expired_platelets_task()

app.conf.beat_schedule = {
    'destroy-expired-donations-every-day': {
        'task': 'myapp.tasks.destroy_expired_donations_task',
        'schedule': 86400,  # Run every day (in seconds)
    },
}