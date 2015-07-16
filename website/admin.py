from django.contrib import admin
from website.models import Order, OrderProduct, Product, ProductPlatform, ProductFeatured, ProductRegion, ProductPrice, ProductStatus, ProductAvailability, ProductType, ProductLanguage, Customer, Supplier, SupplierRelation, ProductStockStatus, ProductStock, ProductPriceCategory, NewsUpdate, Currency, SubCustomer, CustomerBalance

class ProductPlatformAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductPlatform, ProductPlatformAdmin)

class ProductRegionAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductRegion, ProductRegionAdmin)

class ProductStatusAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductStatus, ProductStatusAdmin)

class ProductAvailabilityAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductAvailability, ProductAvailabilityAdmin)

class ProductTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductType, ProductTypeAdmin)

class ProductLanguageAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductLanguage, ProductLanguageAdmin)

class ProductFeaturedAdmin(admin.ModelAdmin):
	list_display = ('product', 'start_date', 'end_date', 'priority', 'created_at', 'updated_at',)
admin.site.register(ProductFeatured, ProductFeaturedAdmin)

class ProductPriceAdmin(admin.ModelAdmin):
	list_display = ('name', 'price_1', 'price_2', 'price_3', 'price_4', 'created_at', 'updated_at',)
admin.site.register(ProductPrice, ProductPriceAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'platform', 'region', 'status', 'availability', 'productType', 'language', 'releaseDate', 'image', 'created_at', 'updated_at',)
	list_filter = ('platform', 'region', 'status', 'availability', 'productType', 'language', 'releaseDate', 'created_at', 'updated_at',)
	search_fields = ('name',)
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('randomId', 'customer', 'customerIp', 'orderStatus', 'created_at', 'updated_at',)
admin.site.register(Order, OrderAdmin)

class OrderProductAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'productStock', 'status', 'quantity', 'price', 'created_at', 'updated_at',)
admin.site.register(OrderProduct, OrderProductAdmin)

class ProductLanguageAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductLanguage, ProductLanguageAdmin)

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('name','businessName', 'url','address','country','emailAddress', 'paypalAccount', 'iban', 'vatId', 'customerLevel', 'customerStatus', 'created_at', 'updated_at',)
	list_filter = ('customerLevel', 'customerStatus', 'created_at', 'updated_at',)
	search_fields = ('name', 'emailAddress','country','customerLevel', 'customerStatus')
admin.site.register(Customer, CustomerAdmin)

class CustomerBalanceAdmin(admin.ModelAdmin):
	list_display = ('customer', 'availableBalance')
	#list_filter = ('customerLevel', 'customerStatus', 'created_at', 'updated_at',)
	search_fields = ('customer', )
admin.site.register(CustomerBalance, CustomerBalanceAdmin)

class SubCustomerAdmin(admin.ModelAdmin):
	list_display = ('name', 'parentCustomer','additionalMargin', 'created_at', 'updated_at',)
admin.site.register(SubCustomer, SubCustomerAdmin)

class SupplierAdmin(admin.ModelAdmin):
	list_display = ('name','businessName', 'url','address','country','emailAddress', 'paypalAccount', 'iban', 'vatId', 'created_at', 'updated_at',)
admin.site.register(Supplier, SupplierAdmin)

class SupplierRelationAdmin(admin.ModelAdmin):
	list_display = ('supplier', 'supplierProduct', 'created_at', 'updated_at',)
admin.site.register(SupplierRelation, SupplierRelationAdmin)

class ProductStockStatusAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at',)
admin.site.register(ProductStockStatus, ProductStockStatusAdmin)

# class ImageInline(admin.TabularInline):
#     model           = ProductStockImage
#     extra = 0

class ProductStockAdmin(admin.ModelAdmin):
	list_display = ('product', 'supplier', 'text', 'stockStatus', 'purchasePrice', 'usesMargin', 'created_at', 'updated_at',)
	list_filter = ('supplier','stockStatus', 'product')
	#search_fields = ('supplier','stockStatus', 'product.name')
	#inlines = (ImageInline, )
admin.site.register(ProductStock, ProductStockAdmin)

#class ProductStockImageAdmin(admin.ModelAdmin):
#	inlines = (ImageInline, )
#	list_display = ('filename',)
#admin.site.register(ProductStockImage, ProductStockImageAdmin)

class NewsUpdateAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'created_at', 'updated_at',)
admin.site.register(NewsUpdate, NewsUpdateAdmin)

class CurrencyAdmin(admin.ModelAdmin):
	list_display = ('name', 'shortName', 'symbol', 'exchangeRate' , 'created_at', 'updated_at',)
admin.site.register(Currency, CurrencyAdmin)