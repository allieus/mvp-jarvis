import os


def environment_variables(request):
    return {
        'FB_APP_ID': os.environ.get('FB_APP_ID', None),
    }
