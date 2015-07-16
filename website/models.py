import PIL.Image as Image
import moneyed
from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django_countries.fields import CountryField

class Supplier(models.Model):
	name = models.CharField(max_length=64)
	businessName = models.CharField(max_length=64, blank=True, null=True, verbose_name='Business')
	url = models.URLField(max_length=200, blank=True, null=True,verbose_name='Website URL')
	address = models.CharField(max_length=128, blank=True, null=True)
	zipCode = models.CharField(max_length=30, blank=True, null=True, verbose_name='Zip Code')
	country = CountryField(blank=True, null=True)
	emailAddress = models.EmailField(max_length=128, verbose_name='Email')
	paypalAccount = models.EmailField(max_length=128, blank=True, null=True, verbose_name='Paypal')
	iban = models.CharField(max_length=32, blank=True, null=True, verbose_name='IBAN')
	vatId = models.CharField(max_length=32, blank=True, null=True, verbose_name='VAT')
	api = models.BooleanField(default=False)
	notes = models.TextField(max_length=1024,blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Supplier"
		verbose_name_plural = "Suppliers"
		ordering = ["name"]

class ProductPlatform(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Platform"
		verbose_name_plural = "Products Platform"
		ordering = ["name"]

class ProductRegion(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Region"
		verbose_name_plural = "Products Region"
		ordering = ["name"]

class ProductStatus(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Status"
		verbose_name_plural = "Products Status"
		ordering = ["name"]

class ProductAvailability(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Availability"
		verbose_name_plural = "Products Availability"
		ordering = ["name"]

class ProductType(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Type"
		verbose_name_plural = "Products Type"
		ordering = ["name"]

class ProductLanguage(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Language"
		verbose_name_plural = "Products Language"
		ordering = ["name"]

class SupplierRelation(models.Model):
	supplier = models.ForeignKey(Supplier)
	supplierProduct = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Supplier Relationship"
		verbose_name_plural = "Suppliers Relationship"
		ordering = ["supplier"]

class ProductPrice(models.Model):
	name = models.CharField(max_length=128)
	price_1 = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Price 1')
	price_2 = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Price 2')
	price_3 = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Price 3')
	price_4 = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Price 4')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = "Products Price"
		verbose_name_plural = "Products Prices"
		ordering = ["name"]

class Product(models.Model):
	name = models.CharField(max_length=128)
	platform = models.ForeignKey(ProductPlatform)
	region = models.ForeignKey(ProductRegion)
	status = models.ForeignKey(ProductStatus)
	availability = models.ForeignKey(ProductAvailability)
	productType = models.ForeignKey(ProductType, verbose_name='Product Type')
	language = models.ForeignKey(ProductLanguage)
	image = models.ImageField(upload_to='images/', blank=True, null=True)
	elitekeysID = models.PositiveIntegerField(blank=True, null=True)
	releaseDate = models.DateField(null=True, blank=True)
	#price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Fixed Sale Price')
	price = models.ForeignKey(ProductPrice)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	def available_stock(self):
		return self.productstock_set.filter(stockStatus=ProductStockStatus.objects.get(name='New')).count()

	class Meta:
		verbose_name = "Product"
		verbose_name_plural = "Products"
		ordering = ["name"]

class ProductBundle(models.Model):
	product = models.ForeignKey(Product)
	amount = models.PositiveIntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.product.name

class ProductFeatured(models.Model):
	product = models.ForeignKey(Product)
	start_date = models.DateField()
	end_date = models.DateField()
	priority = models.PositiveIntegerField(default = 0, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.product.name

	class Meta:
		verbose_name = "Product Featured"
		verbose_name_plural = "Products Featured"
		ordering = ['-priority', 'product']

# class PriceType(models.Model):
# 	name = models.CharField(max_length=128)
# 	marginPercentage = models.DecimalField(max_digits=6,decimal_places=2, default=0)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)

# class ProductPrice(models.Model):
# 	#name = models.CharField(max_length=128)
# 	price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Fixed Sale Price')
# 	product = models.ForeignKey(Product)
# 	priceType = models.ForeignKey(PriceType)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
	
# 	def __unicode__(self):
# 		return self.price

# 	class Meta:
# 		verbose_name = "Product Price"
# 		verbose_name_plural = "Product Prices"
# 		#ordering = ["name"]


class ProductStockStatus(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Product Stock Status"
		verbose_name_plural = "Products Stock Status"
		ordering = ["name"]

class ProductStock(models.Model):
	product = models.ForeignKey(Product)
	supplier = models.ForeignKey(Supplier)
	bundle = models.PositiveIntegerField(blank=True, null=True)
	image = models.ImageField(upload_to='assets/', blank=True, null=True)
	text = models.CharField(max_length=128, blank=True, null=True)
	stockStatus = models.ForeignKey(ProductStockStatus, verbose_name='Status')
	#filename = models.CharField(max_length=256, blank=True, null=True)
	#purchasePrice = models.DecimalField(max_digits=6,decimal_places=2, default=0)
	#fixedPrice = models.DecimalField(max_digits=6,decimal_places=2, default=0)
	purchasePrice = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Supplier Price')
	#fixedPrice = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Fixed Sale Price')
	usesMargin = models.BooleanField( verbose_name='Uses Auto Margin', default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.product.name

	class Meta:
		verbose_name = "Product Code"
		verbose_name_plural = "Products Codes"
		ordering = ["created_at"]

# class ProductStockImage(models.Model):
# 	#productStock = models.ForeignKey(ProductStock)
# 	image = models.ImageField(upload_to='assets', blank=True, null=True)
# 	filename = models.CharField(max_length=256, blank=True, null=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)

# 	def __unicode__(self):
# 		return self.productStock.product.name

# 	class Meta:
# 		verbose_name = "Product Stock Image"
# 		verbose_name_plural = "Product Stock Images"
# 		ordering = ["created_at"]

class ProductPriceCategory(models.Model):
	margin = models.PositiveSmallIntegerField()
	min_range = models.PositiveSmallIntegerField()
	max_range = models.PositiveSmallIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

class CustomerLevel(models.Model):
	name = models.CharField(max_length=64)
	bonusDiscount = models.PositiveSmallIntegerField(default = 0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

class CustomerStatus(models.Model):
	name = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

class Currency(models.Model):
	name = models.CharField(max_length=16)
	shortName = models.CharField(max_length=3)
	symbol = models.CharField(max_length=9)
	exchangeRate = models.DecimalField(max_digits=8, decimal_places = 6, default = 1)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Currency"
		verbose_name_plural = "Currencies"
		ordering = ["name"]

class Customer(models.Model):
	name = models.CharField(max_length=128)
	user = models.OneToOneField(User, null=True)
	#password = models.CharField(max_length=64)
	businessName = models.CharField(max_length=64, blank=True, null=True, verbose_name='Business Name')
	url = models.URLField(max_length=200, blank=True, null=True,verbose_name='Website URL')
	address = models.CharField(max_length=128, blank=True, null=True)
	zipCode = models.CharField(max_length=30, blank=True, null=True, verbose_name='Zip Code')
	country = CountryField()
	emailAddress = models.EmailField(max_length=128, verbose_name='Email')
	paypalAccount = models.EmailField(max_length=128, blank=True, null=True, verbose_name='Paypal')
	iban = models.CharField(max_length=32, blank=True, null=True, verbose_name='IBAN')
	vatId = models.CharField(max_length=32, blank=True, null=True, verbose_name='VAT')
	customerLevel = models.ForeignKey(CustomerLevel, verbose_name='Customer Level', null=True)
	customerStatus = models.ForeignKey(CustomerStatus, verbose_name='Customer Status', null=True)
	defaultCurrency = models.ForeignKey(Currency, verbose_name='Currency')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	def hidden_field_available_balance(self):
		return self.availableBalance

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Customer._meta.fields]

class CustomerBalance(models.Model):
	customer = models.ForeignKey(Customer)
	availableBalance = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Balance')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class SubCustomer(models.Model):
	name = models.CharField(max_length=64)
	parentCustomer = models.ForeignKey(Customer, verbose_name='Parent')
	additionalMargin = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name='Extra Margin')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "Customers Sub"
		verbose_name_plural = "Customers Sub"
		ordering = ["created_at"]

class OrderStatus(models.Model):
	name = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

class Order(models.Model):
	randomId = models.PositiveIntegerField()
	customer = models.ForeignKey(Customer)
	customerIp = models.GenericIPAddressField()
	#orderProducts = models.ForeignKey(OrderProducts)
	#orderTotal = models.ForeignKey(OrderTotal)
	orderStatus = models.ForeignKey(OrderStatus)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.randomId

	class Meta:
		ordering = ["-created_at"]

class OrderTotal(models.Model):
	order = models.ForeignKey(Order, related_name='totals')
	amount = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Amount')
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return str(self.amount)

class OrderProductStatus(models.Model):
	name = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name
		
class OrderProduct(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	productStock = models.ForeignKey(ProductStock, null=True, blank=True)
	status = models.ForeignKey(OrderProductStatus)
	quantity = models.PositiveSmallIntegerField()
	price = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Price')
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.product.name

class PaymentType(models.Model):
	name = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.name

class CustomerTransactions(models.Model):
	customer = models.ForeignKey(Customer)
	order = models.ForeignKey(Order,null=True)
	amount = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Amount')
	runningBalance = MoneyField(max_digits=6, decimal_places=2, default_currency='EUR', verbose_name='Running Balance')
	paymentType = models.ForeignKey(PaymentType)
	transactionID = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.transactionID

	class Meta:
		ordering = ["-created_at"]

class NewsUpdate(models.Model):
	title = models.CharField(max_length=128)
	description = models.TextField(max_length=256)
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "News"
		verbose_name_plural = "News"
		ordering = ["created_at"]

