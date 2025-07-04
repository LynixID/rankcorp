from django import forms
from .models import QuotaPurchase
# forms.py
class QuotaPurchaseForm(forms.ModelForm):
    class Meta:
        model = QuotaPurchase
        fields = ['payment_proof']
        widgets = {
            'payment_proof': forms.ClearableFileInput(attrs={
                'id': 'file-input',  # pastikan id sesuai JS
                'accept': 'image/*',
                'class': 'hidden'
            })
        }

