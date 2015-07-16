from django.conf.urls import url, patterns

urlpatterns = patterns('shopping.views',
    url(r'^add/$', 'add', name='shopping-cart-add'),
    url(r'^removeallthis/$', 'removeallthis', name='shopping-cart-removeallthis'),
    url(r'^remove/$', 'remove', name='shopping-cart-remove'),
    url(r'^show/$', 'show', name='shopping-cart-show'),
    url(r'^empty_cart/$', 'empty_cart', name='shopping-cart-empty'),
    url(r'^update_cart/$', 'update_cart', name='shopping-cart-update-cart'),
)