from django import forms

class FormInventoryAdd(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    category = forms.CharField(max_length=20, required=False)
    unit = forms.CharField(max_length=20, required=False)
    quantity = forms.IntegerField(required=False)
    priceBuy = forms.IntegerField(required=False)

class FormSellCustomer(forms.Form):
    id = forms.IntegerField(required=False)
    cusName = forms.CharField(max_length=100, required=False)
    cusContact = forms.CharField(max_length=20, required=False)
    cusAddress = forms.CharField(max_length=200, required=False)
    cusEmail = forms.EmailField(required=False)
    date = forms.CharField(max_length=200, required=False)
    total = forms.IntegerField(required=False)

class FormSellOrder(forms.Form):
    product = forms.CharField(max_length=100, required=False)
    order_quantity = forms.IntegerField(required=False)
    price_buy = forms.IntegerField(required=False)
    price_sell = forms.IntegerField(required=False)
