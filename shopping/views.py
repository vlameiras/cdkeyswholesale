import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from carton.cart import Cart
from website.models import Product, ProductStock, Customer, ProductAvailability


def get_customer(loggedUser):
	customer = Customer.objects.get(user=loggedUser)
	return customer

def isNum(data):
		try:
			int(data)
			return True
		except ValueError:
			return False

@login_required
def update_cart(request):
	cart = Cart(request.session)


	if request.is_ajax():
		if request.method == 'POST':
			product_id = request.POST.get('id')
			product_qty = request.POST['qty']

			if isNum(product_id) and isNum(product_qty) and product_id > 0 and product_qty >= 0:
				product = Product.objects.get(id=product_id)
				try:
					product_stock_count = ProductStock.objects.filter(product=product).count()
				except ObjectDoesNotExist:
					product_stock_count = 0
					
				is_valid = False
				#print product.availability
				if (product_stock_count > 0 and int(product_qty) > 0 and product_stock_count >= int(product_qty)) or (product.availability == ProductAvailability.objects.get(name='Pre-Order') and int(product_qty) > 0) :							
					cart.remove(product)
					#print product.price
					cart.add(product, price=moneyfield_to_decimal(get_correct_price_based_on_quantity(product, int(product_qty))), quantity=product_qty)
					cart_contents_qty = cart_contents_payload(request)
					is_valid = True
				elif int(product_qty) == 0:
					cart.remove(product)
					cart_contents_qty = cart_contents_payload_unique(request, True, product_id)
				elif int(product_qty) > 0:
					cart_contents_qty = cart_contents_payload_unique(request, True, product_id)
				#elif int(product_qty) > 0 and product.availability == 'Pre-Order':

				html = new_cart_html(request, product_qty)			
				payload = update_cart_status_and_prepare_payload(request, html, cart_contents_qty, is_valid)

				return HttpResponse(json.dumps(payload), content_type="application/json")	
	return HttpResponseRedirect('/')

def get_correct_price_based_on_quantity(product, qty):
	if qty < 10:
		return product.price.price_1
	elif qty < 20:
		return product.price.price_2
	elif qty < 50:
		return product.price.price_3
	else:
		return product.price.price_4
	
def moneyfield_to_decimal(money_field):
	#print money_field
	money_str = str(money_field)
	money_str = money_str.split()
	money_decimal = Decimal(money_str[0])
	return money_decimal 

def add(request):
	cart = Cart(request.session)
	product = Product.objects.get(id=request.GET.get('id'))
	try:
		product_stock = ProductStock.objects.get(product=product)
	except ObjectDoesNotExist:
		product_stock = None
	####ir buscar preco correcto
	cart.add(product, price=2)

	html = new_cart_html(request,0)
	cart_contents_qty = cart_contents_payload(request)
	payload = update_cart_status_and_prepare_payload(request, html, cart_contents_qty, True)

	return HttpResponse(json.dumps(payload), content_type="application/json")


def show(request):
    return render(request, 'show-cart.html')


def remove(request):
	cart = Cart(request.session)
	product_id = request.GET.get('id')
	product = Product.objects.get(id=product_id)
	is_unique = is_product_qty_unique(request, product_id)
	cart.remove_single(product)
	html = new_cart_html(request,0)
	cart_contents_qty = cart_contents_payload_unique(request, is_unique, product_id)
	payload = update_cart_status_and_prepare_payload(request, html, cart_contents_qty, True)
	return HttpResponse(json.dumps(payload), content_type="application/json")


def removeallthis(request):
	cart = Cart(request.session)
	product_id = request.POST.get('id')
	product = Product.objects.get(id=product_id)
	while product in cart:
		cart.remove_single(product)
	html = new_cart_html(request,1)
	cart_contents_qty = cart_contents_payload_unique(request, True, product_id)
	payload = update_cart_status_and_prepare_payload(request, html, cart_contents_qty, True)
	return HttpResponse(json.dumps(payload), content_type="application/json")


def empty_cart(request):
	cart = Cart(request.session)
	cart.clear()
	html = new_cart_html(request,1)
	cart_contents_qty = cart_contents_empty(request)
	payload = update_cart_status_and_prepare_payload(request, html, cart_contents_qty)
	return HttpResponse(json.dumps(payload), content_type="application/json")

def update_cart_status_and_prepare_payload(request, html, cart_quantities, is_valid_operation):
	cart = Cart(request.session)
	customer = get_customer(request.user)
	cart_size = len(cart.items)
	cart_append = 'product'
	if cart_size > 1:
		cart_append = 'products'

	payload = {'total': str(cart.total), 
	'quantity': str(cart_size), 
	'cart_quantities': cart_quantities,
	'append': cart_append, 
	'currency': customer.defaultCurrency.shortName,
	'valid': is_valid_operation,
	'html': html
	}
	return payload

def cart_contents_payload(request):
	cart = Cart(request.session)
	qty_list = {}
	for item in cart.items:
		qty_list[item.product.pk] = item.quantity
	return qty_list

def cart_contents_payload_unique(request, is_unique, product_id):
	cart = Cart(request.session)
	qty_list = {}
	for item in cart.items:
		qty_list[item.product.pk] = item.quantity
	if is_unique:
		qty_list[product_id] = 0
	#print qty_list
	return qty_list

def cart_contents_empty(request):
	cart = Cart(request.session)
	qty_list = {}
	for item in cart.items:
		qty_list[item.product.pk] = 0
	return qty_list

def is_product_qty_unique(request, id):
	cart = Cart(request.session)
	for item in cart.items:
		if str(item.product.pk) == id:
			if item.quantity == 1:
				return True
	return False

def new_cart_html(request, qty):
	cart = Cart(request.session)
	customer = get_customer(request.user)
	html = ''

	for item in cart.items:
		html += '<li role=menu id="' 
		html += str(item.product.pk) 
		html += '"><a role="menuitem" tabindex="-1" href="#" class="deleteAllThisFromCart" id="'
		html += str(item.product.pk) + '"><div style="width: 100%;"> <div style="float: left; "><h6>'		
		html += str(item.quantity) + 'x ' + str(item.product.name) + ' ' + str(item.price) + ' ' 
		html += str(customer.defaultCurrency.shortName) 
		html += '</h6></div><div style="text-align: right;"><h6><strong>&nbsp;&nbsp;<span class="glyphicon glyphicon-remove"></span></strong></h6></div></div></a></li>'
	html += '<li role="menu" class="divider"></li>'
	html += '<li role="menu"><a role="menuitem" tabindex="-1" href="#">'
	html += '<span style="text-align:right;"><h6><strong>Total: </strong>' 
	html += str(cart.total) + str(customer.defaultCurrency.shortName)
	html +='</h6></span></a></li></ul>'
	return html