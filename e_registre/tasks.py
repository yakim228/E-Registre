# from celery import task
# from celery.utils.log import get_task_logger
# from django.conf import settings
# from celery.decorators import task


# logger = get_task_logger(__name__)


# @task(name="search")
# def send_feedback_email_task(search):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("rechecher")
#     return send_feedback_email(search)

# @task(name="sum_two_num")
# def add(x,y):
#     return x+y
