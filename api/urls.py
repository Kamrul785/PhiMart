from django.urls import path, include
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewsSet
from order.views import CartViewSet, CartItemViewSet, OrderViewSet, initialize_payment, payment_success, payment_cancel, payment_fail, HasOrderPorduct

from rest_framework_nested  import routers  

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename= 'carts')
router.register('orders', OrderViewSet, basename= 'orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewsSet, basename='product-image')


cart_router = routers.NestedDefaultRouter(router, 'carts', lookup= 'cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')


# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/', initialize_payment, name='initiate-payment'),
    path('payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_fail, name='payment-fail'),
    path('payment/cancel/', payment_cancel, name='payment-cancel'),
    path('orders/has-ordered/<int:product_id>/', HasOrderPorduct.as_view())
]