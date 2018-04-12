from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DigMetricView, DigPathView

urlpatterns = {
    url(r'^get_dig_metric_graph/$', DigMetricView.as_view(), name="get_dig_metric_graph"),
    url(r'^get_dig_path_graph/$', DigPathView.as_view(), name="get_dig_path_graph"),
}

urlpatterns = format_suffix_patterns(urlpatterns)