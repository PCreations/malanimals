from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from animals.views import (
    AnimalList,
    AnimalDetail
)

urlpatterns = [
    url(r'^$', AnimalList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', AnimalDetail.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)