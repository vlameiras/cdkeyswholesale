# encoding=utf8

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from datetime import date
from website.models import Order, OrderProduct
import re

register = template.Library()

@register.filter
def get_item(dictionary, key):
	val = dictionary.get(key)
	if val is None:
		val = ''
	return val

@register.filter
def get_available_stock(product_id):
	return ''

@register.filter
def get_order_total(totals,order):
	totals_filtered = totals.get(order=order)
	return totals_filtered.amount

@register.filter
def get_additional_spaces(name, max):
	spaces = ' ' * (max - len(name))
	return name + spaces
@register.filter
def get_preorder_release_date(release_date):
	actual_date = date.today()
	if release_date is not None and release_date != '' and release_date > actual_date:
		return release_date
	return None

@register.filter
def get_products_on_order(order):
	order_products = OrderProduct.objects.filter(order=order).distinct('product')
	return order_products

@register.filter
def get_price_with_currency_symbol(price):
	price_str = str(price)
	price_str = price_str.split()
	if price_str[1] == 'EUR':
		return '€'+price_str[0]
	elif price_str[1] == 'USD':
		return '$'+price_str[0]
	elif price_str[1] == 'GBP':
		return '£'+price_str[0]
	return price

@stringfilter
def spacify(value, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))
spacify.needs_autoescape = True
register.filter(spacify)