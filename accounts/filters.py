import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        label="Дата начала",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        label="Дата окончания",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    note = CharFilter(
        field_name="note",
        lookup_expr="icontains",
        label="Комментарий",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по комментарию'})
    )

    class Meta:
        model = Order
        fields = {
            'product': ['exact'],
            'status': ['exact'],
        }
        labels = {
            'product': 'Изделие',
            'status': 'Статус',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем Bootstrap классы к остальным полям
        for field in self.form.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})