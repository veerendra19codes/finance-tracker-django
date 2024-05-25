# tracker/forms.py
from django import forms
from .models import Income, Expense, Budget
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'

class IncomeForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    class Meta:
        model = Income
        fields = ['title','source', 'amount', 'date', 'description']
        widgets = {
            'date': DateInput(attrs={'max': date.today().isoformat()}),
        }

class ExpenseForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    class Meta:
        model = Expense
        fields = ['title','category', 'amount', 'date', 'description']
        widgets = {
            'date': DateInput(attrs={'max': date.today().isoformat()}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit']