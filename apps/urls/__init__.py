from apps.urls.home import urlpatterns as home_url
from apps.urls.order import urlpatterns as order_url
from apps.urls.product import urlpatterns as product_url
from apps.urls.user import urlpatterns as user_url
from apps.urls.market import urlpatterns as market_url
from apps.urls.statistic import urlpatterns as statistic_url
from apps.urls.workers.operator import urlpatterns as operator_url
from apps.urls.workers import test_url

urlpatterns = [
    *home_url,
    *order_url,
    *product_url,
    *user_url,
    *market_url,
    *statistic_url,
    *operator_url,
    *test_url
]
