from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

# router = DefaultRouter()
# router.register(r'orders', OrderViewSet, basename='orders')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# GET /orders/ → list
# POST /orders/ → create
# GET /orders/{id}/ → retrieve
# PUT/PATCH /orders/{id}/ → update
# DELETE /orders/{id}/ → destroy
# GET /orders/my-orders/ → custom action
# POST /orders/{id}/cancel/ → custom action

order_list = OrderViewSet.as_view({'get': 'list', 'post': 'create'})
order_detail = OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('/', order_list, name='order-list'),
    path('/<int:pk>/', order_detail, name='order-detail'),
    path('/my-orders/', OrderViewSet.as_view({'get': 'my_orders'}), name='my-orders'),
    path('/<int:pk>/cancel/', OrderViewSet.as_view({'post': 'cancel_order'}), name='order-cancel'),
]