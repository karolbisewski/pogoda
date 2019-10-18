# import os
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pogoda.settings')
#
# app = Celery('pogoda')
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.autodiscover_tasks()
#
# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(1.0, test.s('hello'), name='add every 10')
#
# @app.task
# def test(arg):
#     print('1')
#     with open('xd', 'w') as f:
#         f.write('1\n')
#
#     print(arg)
#     return "XDDD"
#
