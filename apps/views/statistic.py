import datetime

from django.db.models import Count, Q, Sum
from django.views.generic import ListView, TemplateView

from apps.models import Order, Thread


class StatisticTemplateView(TemplateView):
    template_name = 'apps/statistic/statistic-list.html'

    def get_context_data(self, **kwargs):
        map_range_date = {
            "last_day": (datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()),
            "today": (
                datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), datetime.datetime.now()),
            "yesterday": (
                (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                               microsecond=0),
                (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59,
                                                                               microsecond=999999)),

            "weekly": (datetime.datetime.now() - datetime.timedelta(days=7), datetime.datetime.now()),
            "monthly": (datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()),
        }

        period = self.request.GET.get('period', 'all')
        date = map_range_date.get(period)
        data = super().get_context_data(**kwargs)
        statistics = Thread.objects.filter(user_id=self.request.user.id)
        if date:
            statistics = statistics.filter(thread_orders__ordered_at__range=date)
        statistics = statistics.annotate(
            new_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.NEW)),
            ready_to_order_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.READY_TO_ORDER)),
            delivering_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.DELIVERING)),
            delivered_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.DELIVERED)),
            not_pick_up_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.NOT_PICK_UP)),
            archived_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.ARCHIVED)),
            cancel_count=Count('thread_orders', filter=Q(thread_orders__status=Order.OrderType.CANCEL)),
        ).only('name', 'product__name', 'visit_count')
        tmp = statistics.aggregate(
            all_visit_count=Sum('visit_count'),
            all_new_count=Sum('new_count'),
            all_ready_to_order_count=Sum('ready_to_order_count'),
            all_delivering_count=Sum('delivering_count'),
            all_delivered_count=Sum('delivered_count'),
            all_not_pick_up_count=Sum('not_pick_up_count'),
            all_archived_count=Sum('archived_count'),
            all_cancel_count=Sum('cancel_count'),
        )
        data['statistics'] = statistics
        data['thread_count'] = statistics.count()
        data.update(tmp)
        return data
