import sys
sys.path.insert(0, 'dj')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings.dev")

import azure.functions as func
from dj.wsgi import application

wsgi = func.WsgiMiddleware(app=application)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return wsgi.main(req, context)
