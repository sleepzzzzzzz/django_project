from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone','email', 'address', 'buying_type', 'order_date', 'comment'
        )
