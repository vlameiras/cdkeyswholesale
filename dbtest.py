from django.db import connections, connection, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ConnectionDoesNotExist
from django.contrib.auth.models import User
from django.core.management import call_command
from website import models
from website.models import PaymentType, OrderProductStatus, Product, ProductPrice, ProductPlatform, ProductRegion, ProductStatus, ProductAvailability, ProductType, ProductLanguage, ProductStatus, Supplier, ProductStockStatus, Customer, CustomerBalance, CustomerLevel, CustomerStatus, Currency, OrderStatus
from moneyed import Money, EUR, USD
from djmoney.models.fields import MoneyField

def setup_cursor_elitegames():
    try:
        cursor = connections['elitegames_prd'].cursor()
        return cursor
    except ConnectionDoesNotExist:
        print "elitegames database is not configured"
        return None

def setup_cursor_local():
    try:
        cursor = connections['default'].cursor()
        return cursor
    except ConnectionDoesNotExist:
        print "elitegames database is not configured"
        return None


def insertPlatforms():
    ProductPlatform.objects.bulk_create([
        ProductPlatform(name='Steam'),
        ProductPlatform(name='Origin'),
        ProductPlatform(name='Uplay'),
        ProductPlatform(name='Battle.net'),
        ProductPlatform(name='Xbox Live'),
        ProductPlatform(name='PSN'),
        ProductPlatform(name='GOG'),
        ProductPlatform(name='Official Website'),
        ProductPlatform(name='Retail'),
        #ProductPlatform(name='Multi'),
    ])

def insertRegions():
    ProductRegion.objects.bulk_create([
        ProductRegion(name='Worldwide'),
        ProductRegion(name='Europe'),
        ProductRegion(name='U.S.A'),
        ProductRegion(name='Russia'),
        ProductRegion(name='Poland'),
        ProductRegion(name='Asia'),
    ])

def insertLanguages():
    ProductLanguage.objects.bulk_create([
        ProductLanguage(name='Multi'),
        ProductLanguage(name='English'),
        ProductLanguage(name='Russian'),
    ])

def insertStatuses():
    ProductStatus.objects.bulk_create([
        ProductStatus(name='Enabled'),
        ProductStatus(name='Disabled')
    ])

def insertProductStockStatuses():
    ProductStockStatus.objects.bulk_create([
        ProductStockStatus(name='New'),
        ProductStockStatus(name='Used')
    ])


def insertAvailability():
    ProductAvailability.objects.bulk_create([
        ProductAvailability(name='Available'),
        ProductAvailability(name='Out of Stock'),
        ProductAvailability(name='Pre-Order'),
        ProductAvailability(name='On Request'),
    ])

def insertTypes():
    ProductType.objects.bulk_create([
        ProductType(name='Game'),
        ProductType(name='DLC'),
        ProductType(name='Game Card'),
    ])

def insertSuppliers():
    Supplier.objects.bulk_create([
        Supplier(name='GamePointsNow'),
        Supplier(name='CDKey24'),
        Supplier(name='CodesWholesale'),
        Supplier(name='Gunther'),
        Supplier(name='UGK'),
        Supplier(name='Battlekeys'),
        Supplier(name='Click Ent'),
        Supplier(name='Kinguin'),
        Supplier(name='G2A'),
    ])

def insertCurrencies():
    Currency.objects.bulk_create([
        Currency(name='Euro', shortName='EUR', symbol='&euro;', exchangeRate=1.000000),
        Currency(name='US Dollar', shortName='USD', symbol='&#36;', exchangeRate=1.100000),
        Currency(name='British Pound', shortName='GBP', symbol='&pound;', exchangeRate=0.800000),
    ])

def insertCustomerLevels():
    CustomerLevel.objects.bulk_create([
        CustomerLevel(name='Wholesale'),
        CustomerLevel(name='Admin'),
    ])

def insertCustomerStatus():
    CustomerStatus.objects.bulk_create([
        CustomerStatus(name='Active'),
        CustomerStatus(name='Inactive'),
        CustomerStatus(name='Suspended'),
    ])

def insertOrderStatuses():
    OrderStatus.objects.bulk_create([
        OrderStatus(name='Completed'),
        OrderStatus(name='Pre-Order'),
        OrderStatus(name='Canceled'),
        OrderStatus(name='Pending'),
        OrderStatus(name='Processing'),
    ])

def insertOrderProductStatuses():
    OrderProductStatus.objects.bulk_create([
        OrderProductStatus(name='Completed'),
        OrderProductStatus(name='Pre-Order'),
        OrderProductStatus(name='Processing'),
    ])

def insertPaymentTypes():
    PaymentType.objects.bulk_create([
        PaymentType(name='Paypal'),
        PaymentType(name='Paypal Mass Payment'),
        PaymentType(name='Balance'),
        PaymentType(name='Order'),
    ])

def insertCustomers():
    Customer.objects.bulk_create([
        Customer(name='elitegames', 
            user = User.objects.get(username='me'), 
            businessName = 'elitegame.com', 
            url = 'http://www.elitegame.com', 
            address ='Rua dos Tateus 1', 
            zipCode ='2000', 
            country ='PT',
            emailAddress = 'me@gmail.com', 
            paypalAccount = 'me@gmail.com', 
            vatId = 'PT222222220', 
            customerLevel = CustomerLevel.objects.get(name='Wholesale'),
            customerStatus = CustomerStatus.objects.get(name='Active'), 
            defaultCurrency = Currency.objects.get(shortName='EUR')),
    ])
    CustomerBalance.objects.bulk_create([
        CustomerBalance(
        customer = Customer.objects.get(name='elitegames'),
        availableBalance = 1350.50),
    ])

def import_games_names():
    cursor = setup_cursor_elitegames()
    if cursor is None:
        return
    sql = """SELECT a.product_id, b.name, a.price FROM product a, product_description b where b.product_id = a.product_id and b.language_id = 1 and a.status = 1 order by b.name """
    cursor.execute(sql)
    insert_list = []

    for row in cursor.fetchall():
        print row[0]
        nameRow = stripPlatform(row[1])
        priceRow = float(row[2])
        insert_list.append(Product(
            name = nameRow,
            platform = ProductPlatform.objects.get(name=getGamePlatform(row[0])),
            region = ProductRegion.objects.get(name='Worldwide'),
            status = ProductStatus.objects.get(name=getGameStatus(row[0])),
            availability = ProductAvailability.objects.get(name=getGameAvailability(row[0])),
            productType = ProductType.objects.get(name='Game'),
            language = ProductLanguage.objects.get(name='Multi'),
            price = ProductPrice.objects.create(name=nameRow,price_1=Money(str(priceRow),"EUR"),price_2=Money(str(priceRow / 1.02),"EUR"),price_3=Money(str(priceRow / 1.03),"EUR"),price_4=Money(str(priceRow / 1.05),"EUR")),
            elitegamesID = row[0],))

    Product.objects.bulk_create(insert_list)

    sql = """SELECT a.product_id, a.price FROM product_special a, product b where a.product_id = b.product_id AND b.status = 1 AND customer_group_id = 8 """
    cursor.execute(sql)
    insert_list = []

    for row in cursor.fetchall():    
        priceRow = float(row[1])
        product = Product.objects.get(elitegamesID=str(row[0]))
        product.price.price_1 = Money(str(priceRow / 1), "EUR")
        product.price.price_2 = Money(str(priceRow / 1.02), "EUR")
        product.price.price_3 = Money(str(priceRow / 1.03), "EUR")
        product.price.price_4 = Money(str(priceRow / 1.05), "EUR")
        product.price.save()
        product.save()

    sql = """SELECT a.product_id, a.price FROM product_special a, product b where a.product_id = b.product_id AND b.status = 1 AND customer_group_id = 6 """
    cursor.execute(sql)
    insert_list = []

    for row in cursor.fetchall():       
        priceRow = float(row[1])
        product = Product.objects.get(elitegamesID=str(row[0]))
        product.price.price_1 = Money(str(priceRow / 1), "EUR")
        product.price.price_2 = Money(str(priceRow / 1.02), "EUR")
        product.price.price_3 = Money(str(priceRow / 1.03), "EUR")
        product.price.price_4 = Money(str(priceRow / 1.05), "EUR")
        product.price.save()
        product.save()

def stripPlatform(product):
    product = product.replace('Steam', '')
    product = product.replace('EA Origin', '')
    product = product.replace('Origin', '')
    product = product.replace('Uplay', '')
    product = product.replace('Key', '')
    product = product.replace('&amp;', '&')
    #product = product.replace('Xbox Live', '')
    return product

def getGamePlatform(productId):
    cursor = setup_cursor_elitegames()
    sql = """SELECT a.category_id FROM product_to_category a where a.product_id = """ + str(productId)
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] == 60:
            return 'Steam'
        elif row[0] == 61:
            return 'Origin'
        elif row[0] == 70:
            return 'Uplay'
        elif row[0] == 63:
            return 'Battle.net'
        elif row[0] == 36:
            return 'Xbox Live'
        elif row[0] == 69:
            return 'PSN'
        elif row[0] == 62 or row[0] == 52:
            return 'Official Website'


def getGameStatus(productId):
    cursor = setup_cursor_elitegames()
    sql = """SELECT a.status FROM product a where a.product_id = """ + str(productId)
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] == 0:
            return 'Disabled'
        elif row[0] == 1:
            return 'Enabled'

def fill_data_tables():
    #cursor_elitegames = setup_cursor_elitegames()

    insertPlatforms()
    insertRegions()
    insertLanguages()
    insertStatuses()
    insertAvailability()
    insertTypes()
    insertSuppliers()
    insertProductStockStatuses()

    insertCurrencies()
    insertCustomerLevels()
    insertCustomerStatus()
    insertCustomers()

    insertOrderStatuses()
    insertOrderProductStatuses()
    insertPaymentTypes()

def getGameAvailability(productId):
    cursor = setup_cursor_elitegames()
    sql = """SELECT a.category_id FROM product_to_category a where a.product_id = """ + str(productId)
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] == 64:
            return 'Pre-Order'
    return 'Available'

def main():
    call_command('syncdb', interactive=True)

    fill_data_tables()
    import_games_names()

if __name__=="__main__":
    main()
