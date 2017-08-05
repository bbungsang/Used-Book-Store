import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.debug')
app = Celery('used-book-store')

##
# - namespace 는 대문자로
#       settings 에서 CELERY_ 로 시작하는 설정만 가져오게 된다.
# - 어떤 함수를 처리하기 위해서 해당 함수를 celery 에 등록해야한다.
#       등록한 것을 어떻게 인식하게 하느냐? INSTALLED_APPS 의 내용을 app.authdiscover_tasks() 를 통해서 가져온다.
#       어플리케이션 tasks 파일 안의 내용을 가져와서 celery 안 쪽에 인식하게 해준다.
##
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))