from django.urls import path
from . import views 


urlpatterns = [
    path("plans/", views.getAdvertisingPlans, name="advertisingPlans"),
    path("orders/order/create/",views.createOrder, name="createOrder"),
    path("order/my/",views.getMyOrders, name="getMyOrders"),
    path("orders/all/", views.getAllOrders, name="getAllOrders"),
    path("orders/order/id/<str:id>/", views.getOrderById, name="getOrderById"),
    path("orders/order/pay/<str:id>/", views.updateOrderToPaid, name="updateOrderToPaid"),
    
    
]