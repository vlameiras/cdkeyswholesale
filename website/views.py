import os, mimetypes, urllib
import sys
import boto
import random
import json
import zipfile
import StringIO
import tempfile
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
#from StringIO import StringIO
from django.utils import timezone
from website.models import CustomerTransactions, PaymentType, Order, ProductFeatured, OrderProduct, OrderProductStatus, OrderStatus, OrderTotal, Product, ProductPlatform, ProductRegion, ProductLanguage, ProductAvailability, ProductStock, ProductStockStatus, Supplier, Customer, CustomerBalance
from website.forms import RegisterForm, ProfileForm
from carton.cart import Cart
from jfu.http import upload_receive, UploadResponse, JFUResponse
from boto.s3.key import Key

def get_text_codes_file(text_codes):
	temp = tempfile.NamedTemporaryFile(mode='w+t', prefix="text_", suffix=".txt", delete=False)
	try:
		for text_code in text_codes:
			text_code = text_code.replace('\n', '')
			temp.write(text_code)
		temp.seek(0)
		#for line in temp:
			#print line.rstrip()
	finally:
		temp.close()
		return temp

@login_required
def download_codes(request):
	# Files (local path) to put in the .zip
	# FIXME: Change this (get paths from DB etc)
	order_random_id = request.GET.get('order')
	product_id = request.GET.get('product')
	customer = Customer.objects.get(user=request.user)
	try:
		product = Product.objects.get(pk=product_id)
		order = Order.objects.get(randomId=order_random_id, customer=customer)
		

		if product is not None and order is not None:
			order_products = OrderProduct.objects.filter(order=order,product=product)
			if order_products is not None:
				filenames = []
				text_codes = []
				for order_product in order_products:
					#ProductStock.objects.all()[0]
					product_stock =  order_product.productStock
					print product_stock.image
					if product_stock.image is not None and product_stock.image != "":
						filenames.append(settings.MEDIA_ROOT + product_stock.image.url)
					elif product_stock.text is not None and product_stock.text != "":
						text_codes.append(product_stock.text)
				# Folder name in ZIP archive which contains the above files
				# E.g [thearchive.zip]/somefiles/file2.txt
				# FIXME: Set this to something better
				if len(text_codes) > 0:
					text_file = get_text_codes_file(text_codes)
					filenames.append(text_file.name)
				zip_subdir = product.name
				#zip_filename = "%s.zip" % zip_subdir
				zip_filename = order_random_id + ".zip"

				# Open StringIO to grab in-memory ZIP contents
				s = StringIO.StringIO()

				# The zip compressor
				zf = zipfile.ZipFile(s, "w")

				for fpath in filenames:
					# Calculate path for file in zip
					fdir, fname = os.path.split(fpath)
					zip_path = os.path.join(zip_subdir, fname)
					zf.write(fpath, zip_path)
					# Add file, at correct path
					

				# Must close zip for all contents to be written
				zf.close()

				# Grab ZIP file from in-memory, make response with correct MIME-type
				resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
				# ..and correct content-disposition
				resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

				return resp
	except:
		print sys.exc_info()[0]
		print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
	return HttpResponseRedirect('/account/#orders')

@login_required
def index(request):
	products_featured = get_all_products_featured()
	products = get_all_products()
	products = remove_products_featured(products, products_featured)
	platforms = get_all_platforms()
	regions = get_all_regions()
	languages = get_all_languages()
	availabilities = get_all_availabilities()
	productsStock = get_all_products_stock()
	customer = get_customer(request.user)
	customer_balance = get_customer_balance(customer)
	cart = Cart(request.session)
	cart_count = cart.total
	cart_contents_qty = cart_contents_payload(request)

	return render(request, 'website/index.html', 
		{'products': products,
		'products_featured': products_featured,
		'platforms': platforms, 
		'regions': regions, 
		'languages': languages, 
		'availabilities': availabilities,
		'productsStock': productsStock,
		'customer': customer,
		'customer_balance': customer_balance,
		'cart': cart,
		'cart_product_count': cart_count,
		'cart_contents_qty': cart_contents_qty,
		})

@login_required
def get_order_products(request):
	if request.is_ajax():
			if request.method == 'POST':
				customer = get_customer(request.user)
				order_id = request.POST.get('id')
				try:
					filter_args = {'randomId': order_id, 'customer': customer}
					order = Order.objects.filter(**filter_args)
					if order.count() > 0:
						#order_products = OrderProducts.objects.get(order=order)
						#html = generate_order_html(order_products)
						html = '12345'
						payload = ajax_payload(html)
						return HttpResponse(json.dumps(payload), content_type="application/json")
					else:
						return HttpResponseRedirect('/')
				except ObjectDoesNotExist:
					product_stock = None

@login_required
def checkout(request):
	customer = get_customer(request.user)
	customer_balance = get_customer_balance(customer)
	available_balance = customer_balance.availableBalance
	cart = Cart(request.session)

	#create_order_products(cart, 1)
	try:
		if cart.count == 0:
			messages.error(request, 'You cannot checkout with an empty cart.')
			return HttpResponseRedirect('/')
		
		if request.method == 'POST':
			if request.POST.get("submit_btn") and cart_is_valid(cart) is True and cart.total <= available_balance:
				messages.success(request, 'Order Placed!')

				#testar com moedas diferentes
				customer_balance.availableBalance -= cart.total
				customer_balance.save()

				order_status_complete = OrderStatus.objects.get(name='Completed')
				payment_type = PaymentType.objects.get(name='Order')

				order = Order.objects.create(randomId = get_random_order_number(),
					customer = customer, 
					customerIp = get_client_ip(request),
					orderStatus = order_status_complete)
				order.save()

				order_total = OrderTotal.objects.create(order = order,
					amount = cart.total)
				order_total.save()

				create_order_products(cart, order.randomId)

				CustomerTransactions.objects.create(customer=customer,
					order = order,
					amount = cart.total * -1,
					paymentType = payment_type,
					runningBalance = customer_balance.availableBalance,
					transactionID = get_random_transaction_number())

				cart.clear()
				#redirect to order and get download
				#notify
				return HttpResponseRedirect('/account/#orders')
			else:
				#print request.method
				if cart.total > available_balance:
					messages.error(request, 'You cannot complete this order due to insufficient balance.')
				if cart_is_valid(cart) is False:
					messages.error(request, 'The product(s) you are trying to purchase do not have sufficient quantity. Please return to the <a href="/"><strong>games list</strong></></a> and review your cart.')
				return HttpResponseRedirect('/')
	except:	
		print sys.exc_info()[0]
		print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
		return HttpResponseRedirect('/')

	return render(request, 'website/checkout.html',{ 
		'customer': customer,
		'customer_balance': customer_balance,
		'cart': cart,
		})

@login_required
def account(request):
	customer = get_customer(request.user)
	customer_balance = get_customer_balance(customer)
	cart = Cart(request.session)
	cart_count = cart.total
	orders = Order.objects.filter(customer=customer)
	transactions = CustomerTransactions.objects.filter(customer=customer)
	if request.method == 'POST':
		form = ProfileForm(request.POST,instance=customer)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile details updated.')
			return HttpResponseRedirect('/account/')
	else:
		form = ProfileForm(instance=customer)
	return render(request, 'website/account.html',{'form': form, 
		'customer': customer,
		'customer_balance': customer_balance,
		'cart': cart,
		'cart_product_count': cart_count,
		'orders': orders,
		'transactions': transactions,})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Registration successfully completed. Pending review approval.')
			return HttpResponseRedirect('/')
	else:
		data = {'url': 'http://', }
		form = RegisterForm(initial=data)
	return render(request, 'website/register.html',{'form': form})

def insert_code_text(product, supplier, price, bundle, margin, stockStatus, text):
	instance = ProductStock(product=product, 
		supplier = supplier, 
		purchasePrice = price,
		bundle = bundle,
		stockStatus = stockStatus ,
		text=text)
	instance.save()

def insert_code_image(product, supplier, price, bundle, margin, stockStatus, image):
	instance = ProductStock(product=product, 
		supplier = supplier, 
		purchasePrice = price,
		bundle = bundle,
		stockStatus = stockStatus ,
		image=image)
	instance.save()

@require_POST
@login_required
def upload( request ):

	# The assumption here is that jQuery File Upload
	# has been configured to send files one at a time.
	# If multiple files can be uploaded simulatenously,
	# 'file' may be a list of files.
	file = upload_receive( request )
	basename = file.name

	product_id =  request.POST.get('product_id')
	print product_id
	product = Product.objects.get(pk=product_id)
	supplier_id = request.POST.get('supplier_id')
	supplier = Supplier.objects.get(pk=supplier_id)
	bundle = request.POST.get('bundle')
	price = request.POST.get('price')
	margin = request.POST.get('margin')
	stockStatus = ProductStockStatus.objects.get(name='New')

	if '.txt' in basename:
		for l in file:
			li = l.split('\t')
			try:
				#print li[0]
				insert_code_text(product, supplier, price, bundle, margin, stockStatus, li[0])
			except IndexError:
				print 'Error Inserting Image'
	else:
		insert_code_image(product, supplier, price, bundle, margin, stockStatus, file)

	#for key, value in request.POST.iteritems():
		#print key + ": " + value
	#basename = os.path.basename( instance.file.path )
	#basename = file.name  

	#push_picture_to_s3(settings.MEDIA_ROOT + 'assets/' + file.name, file.name)

	file_dict = {
		'name' : basename,
		'size' : file.size,

		'url': settings.MEDIA_URL + basename,
		'thumbnailUrl': settings.MEDIA_URL + basename,

		#'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
		'deleteType': 'POST',
	}

	return UploadResponse( request, file_dict )

@require_POST
def upload_delete( request, pk ):
	success = True
	try:
		instance = ProductStockImage.objects.get( pk = pk )
		os.unlink( instance.file.path )
		instance.delete()
	except ProductStockImage.DoesNotExist:
		success = False

	return JFUResponse( request, success )

@login_required
def uploader(request):
	#print request.user
	if request.user and str(request.user) == 'vasco':
		products = get_all_products()
		suppliers = get_all_suppliers()
		return render(request, 'website/uploader.html', 
			{'products': products,
			'suppliers': suppliers,
			})
	else:
		return HttpResponseRedirect('/')

def push_picture_to_s3(file_path, file_name, fileInstance):
  try:
	# set boto lib debug to critical
	#logging.getLogger('boto').setLevel(logging.CRITICAL)
	bucket_name = settings.BOTO_S3_BUCKET
	# connect to the bucket
	conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(bucket_name)
	# go through each version of the file
	#key = file_name % id
	#fn = file_path % id
	# create a key to keep track of our file in the storage 
	k = Key(bucket)
	k.key = file_name
	k.set_contents_from_filename(file_path)
	# we need to make it public so it can be accessed publicly
	# using a URL like http://s3.amazonaws.com/bucket_name/key
	#k.make_public()
	# remove the file from the web server
	#os.remove(file_path)
  except:
	print settings.AWS_ACCESS_KEY_ID + ' ' +  settings.AWS_SECRET_ACCESS_KEY
	print sys.exc_info()[0]
	print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)

def get_all_products():
	products = Product.objects.all().order_by('name')
	return products

def remove_products_featured(products, products_featured):
	for product_featured in products_featured:
		#print product_featured.product.pk
		products = products.exclude(id = product_featured.product.pk)
	#print products
	return products

def get_all_products_featured():
	startdate = timezone.now()
	#print startdate
	products_featured = ProductFeatured.objects.filter(start_date__lte=startdate, end_date__gte=startdate)
	#print products_featured
	return products_featured

def get_product_max_name_size(products):
	name = ''
	for product in products:
		if len(product.name) > len(name):
			name = product.name
	return len(name)

def get_platform_max_name_size(platforms):
	name = ''
	for platform in platforms:
		if len(platform.name) > len(name):
			name = platform.name
	return len(name)

def get_all_platforms():
	platforms = ProductPlatform.objects.all().order_by('name')
	return platforms

def get_all_regions():
	regions = ProductRegion.objects.all().order_by('name')
	return regions

def get_all_languages():
	languages = ProductLanguage.objects.all().order_by('name')
	return languages

def get_all_availabilities():
	availabilities = ProductAvailability.objects.all().order_by('name')
	return availabilities

def get_all_products_stock():
	productsStock = ProductStock.objects.all().order_by('purchasePrice')
	return productsStock

def get_all_suppliers():
	suppliers = Supplier.objects.all().order_by('name')
	return suppliers

def get_customer(loggedUser):
	customer = Customer.objects.get(user=loggedUser)
	return customer

def get_customer_balance(customer):
	customer_balance = CustomerBalance.objects.get(customer=customer)
	return customer_balance

def cart_contents_payload(request):
	cart = Cart(request.session)
	qty_list = {}
	for item in cart.items:
		qty_list[item.product.pk] = item.quantity
	return qty_list

def cart_is_valid(cart):
	for item in cart.items:
		product = Product.objects.get(id = str(item.product.pk))
		#product_stock = ProductStock.objects.filter(pk = str(item.product.pk)).filter(stockStatus=ProductStockStatus.objects.get(name='New'))
		cart_item_quantity = item.to_dict().get('quantity')
		#print product.name +' '+ product.availability.name
		if (product.status.name == 'Disabled') or (cart_item_quantity > product.available_stock() and product.availability.name != 'Pre-Order'):		
			return False
	return True

def get_random_order_number():
	order_number = random.randint(1,9999999)
	order = Order.objects.filter(randomId = order_number)
	if order.count() > 0:
		#print order_number
		order_number = get_random_order_number()
	return order_number

def get_random_transaction_number():
	transaction_number = random.randint(1,9999999)
	transaction = CustomerTransactions.objects.filter(transactionID = transaction_number)
	if transaction.count() > 0:
		#print order_number
		transaction_number = get_random_transaction_number()
	return transaction_number

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_order_products(cart, order_id):
	try:
		if cart_is_valid(cart) is True:
	 		for item in cart.items:

	 			cart_item_quantity = item.to_dict().get('quantity')	
	 			product = Product.objects.get(id=item.product.pk)
		 		product_stock_used = ProductStockStatus.objects.get(name='Used')
		 		product_stock = ProductStock.objects.filter(product=product).filter(stockStatus=ProductStockStatus.objects.get(name='New')).order_by('id')

		 		#testar product availability, tem de se ver se e pre-order e criar alternativa
		 		#tem de se avaliar se e On Request antes de criar order, apenas envia email noutra view

		 		for i in range(0,cart_item_quantity):
		 			if product.availability == ProductAvailability.objects.get(name='Pre-Order'):
						ostock_status = OrderProductStatus.objects.get(name='Pre-Order')
						pstock = None
					else:
						ostock_status = OrderProductStatus.objects.get(name='Completed')
						pstock = ProductStock.objects.get(pk=product_stock.first().pk)
						#print str(pstock.pk)
						pstock.stockStatus = product_stock_used
						pstock.save()

					order_product = OrderProduct.objects.create(
						order = Order.objects.get(randomId=order_id),
						productStock = pstock,
						product = product,
						quantity = cart_item_quantity,
						status = ostock_status,
						price = item.price)
					order_product.save()
			return True
	except:
			print sys.exc_info()[0]
			print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
	return False

def generate_order_html(order_products):
	html = '<div>'
	for product in products:
		html += product.productStock.product.name
		html += '<br/>'
	html += '</div>'
	return html

def ajax_payload(html):
	payload = {
		'html': html
	}
	return payload