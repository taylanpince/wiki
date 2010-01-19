import os
import sys

sys.path.append("/home/taylan/sites/wiki/app")
sys.path.append("/home/taylan/sites/wiki/app/lib")
sys.path.append("/home/taylan/sites/wiki/app/wiki")

os.environ["DJANGO_SETTINGS_MODULE"] = "wiki.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
