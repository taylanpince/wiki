from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # Wiki
    (r'', include('doc_wiki.urls')),
)
