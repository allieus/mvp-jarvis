import sys
import logging

import azure.functions as func
import django


sys.path.insert(0, '..')
django.setup()


def main(mytimer: func.TimerRequest) -> None:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_count = User.objects.all().count()

    logging.info(f'Python timer trigger function ran : user_count = {user_count}')
