from django import forms
import models

class ReferralForm(forms.ModelForm):
    class Meta:
        model = models.Referral
        fields = ('title', 'url', 'code', 'info', 'company', 'validity', 'category')
        widgets = {
                'validity': forms.TextInput(attrs={'type': 'date'}),
        }

class YayOrNayForm(forms.ModelForm):
    class Meta:
        model = models.Referral
        fields = ('yay', 'nay', )
