from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime

from.models import Product, Sell, Order
from .forms import FormInventoryAdd, FormSellCustomer, FormSellOrder
from django.contrib.auth import logout


# Create your views here.
@login_required(login_url='home')
def db_home(request):

    sells = Sell.objects.all()
    dates, totals = sell_30(sells)
    orders = Order.objects.all()
    categories, counts = product_types(orders)
    return render(request, "td_database/dashboard.html", {'dates': dates,
                                                          'totals': totals,
                                                          'categories': categories,
                                                          'counts': counts})

def sell_30(sells):
    today = str(datetime.datetime.now()).split(' ')[0]
    current_year, current_month, current_date = today.split('-')
    transactions = {}

    for sell in sells:
        if sell.total is not None:
            date = str(sell.date).split(' ')[0]
            year, month, date = date.split('-')
            if month == current_month and year == current_year:
                g_date = f'{year}-{month}-{date}'

                g_total = sell.total if sell.total is not None else 0

                if g_date not in transactions:
                    transactions[g_date] = g_total
                else:
                    transactions[g_date] += g_total

    dates = list(transactions.keys())
    totals = list(transactions.values())

    return [dates, totals]

def product_types(orders):
    type_counts = {}
    for order in orders:
        product_category = order.product.category
        if product_category not in type_counts:
            type_counts[product_category] = 1
        else:
            type_counts[product_category] += 1

    categories = list(type_counts.keys())
    counts = list(type_counts.values())
    return categories, counts


@login_required(login_url='home')
def db_addrecord(response):
    if response.method == "POST":

        data = response.POST
        sellObj = Sell.objects.get(id=data['id'])
        sellObj.cusName = data['cusName']
        sellObj.cusContact = data['cusContact']
        sellObj.cusAddress = data['cusAddress']
        sellObj.cusEmail = data['cusEmail']
        sellObj.save()

        formSell = FormSellCustomer(initial={'cusName' : sellObj.cusName,
                                             'cusContact': sellObj.cusContact,
                                             'cusAddress': sellObj.cusAddress,
                                             'cusEmail': sellObj.cusEmail})

        formOrder = FormSellOrder()
        formSell.fields["id"].initial = sellObj.id
        formSell.fields["date"].initial = str(sellObj.date).split('.')[0]


        if 'btn_search' in data:
            products = Product.objects.all()
            if products.filter(name=data['product']):
                product = Product.objects.get(name=data['product'])
                if int(data['order_quantity']) <= product.quantity:
                    formOrder = FormSellOrder(initial={'product': product.name,
                                                       'order_quantity': data['order_quantity'],
                                                       'price_buy': product.priceBuy,
                                                       'price_sell': product.priceBuy})
                    print(formOrder)

        if 'btn_update' in data:
            products = Product.objects.all()
            if products.filter(name=data['product']):
                product = Product.objects.get(name=data['product'])
                orderObj = Order(product=product,
                                 sell=sellObj,
                                 order_quantity=data['order_quantity'],
                                 price_buy=product.priceBuy,
                                 price_sell=data['price_sell'],
                                 price_total=int(data['order_quantity'])*int(data['price_sell']))
                product.quantity -= int(data['order_quantity'])
                product.save()
                orderObj.save()

    else:
        sellObj = Sell()
        sellObj.save()

        formSell = FormSellCustomer()
        formOrder = FormSellOrder()
        formSell.fields["id"].initial = sellObj.id
        formSell.fields["date"].initial = str(sellObj.date).split('.')[0]


    sellObj.total = calculate_total_cost(sellObj.order_set.all())
    sellObj.save()
    formSell.fields["total"].initial = sellObj.total
    sells = Sell.objects.all()
    products = Product.objects.all()
    orders = sellObj.order_set.all()
    return render(response, "td_database/addrecord.html", {'formSell': formSell,
                                                           'formOrder': formOrder,
                                                           'orders': orders,
                                                           'products': products,
                                                           'sells': sells})

def calculate_total_cost(orders):
    total = 0
    for order in orders:
        total += order.price_total

    return total

@login_required(login_url='home')
def db_records(response):
    clear_null_sells()
    sells = Sell.objects.all()
    return render(response, "td_database/records.html", {'sells': sells})


@login_required(login_url='home')
def db_inventory(response):
    if response.method == "POST":
        form = FormInventoryAdd(response.POST)
        if form.is_valid():
            exData = form.cleaned_data

            try:
                product = Product.objects.get(name=exData['name'])
                pID = product.id
                product = Product(id=pID,
                                  name=exData['name'],
                                  category=exData['category'],
                                  unit=exData['unit'],
                                  quantity=exData['quantity'] + product.quantity,
                                  priceBuy=exData['priceBuy'])
                product.save()

            except:
                product = Product(name=exData['name'],
                                  category=exData['category'],
                                  unit=exData['unit'],
                                  quantity=exData['quantity'],
                                  priceBuy=exData['priceBuy'])
                product.save()

    form = FormInventoryAdd()
    products = Product.objects.all()
    return render(response, "td_database/inventory.html", {'products' : products,
                                                           'form' : form})

def db_logout(response):
    logout(response)
    return redirect('home')

def clear_null_sells():
    sells = Sell.objects.all()
    for sell in sells:
        if sell.total == None or sell.total == 0:
            sell.delete()
