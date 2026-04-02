from django import forms
from .models import Report

PROVINCE_CHOICES = [
    ('', 'Select Province'),
    ('EC', 'Eastern Cape'),
    ('FS', 'Free State'),
    ('GP', 'Gauteng'),
    ('KZN', 'KwaZulu-Natal'),
    ('LP', 'Limpopo'),
    ('MP', 'Mpumalanga'),
    ('NC', 'Northern Cape'),
    ('NW', 'North West'),
    ('WC', 'Western Cape'),
]
MUNICIPALITY_CHOICES = [
    ('', 'Select Municipality'),
    # Eastern Cape
    ('EC_BUF', 'Buffalo City'),
    ('EC_NMA', 'Nelson Mandela Bay'),
    # Free State  
    ('FS_MAN', 'Mangaung'),
    # Gauteng
    ('GP_JHB', 'City of Johannesburg'),
    ('GP_TSH', 'City of Tshwane'),
    ('GP_EKU', 'Ekurhuleni'),
    # KwaZulu-Natal
    ('KZN_ETH', 'eThekwini'),
    ('KZN_UMG', 'uMgungundlovu'),
    # Limpopo
    ('LP_POL', 'Polokwane'),
    # Mpumalanga
    ('MP_MBU', 'Mbombela'),
    # Northern Cape
    ('NC_SOL', 'Sol Plaatje'),
    # North West
    ('NW_MAF', 'Mahikeng'),
    # Western Cape
    ('WC_CPT', 'City of Cape Town'),
    ('WC_GEO', 'Garden Route'),
]

class ReportForm(forms.ModelForm):
    province = forms.ChoiceField(
        choices=PROVINCE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'province-select'})
    )
    
    municipality = forms.ChoiceField(
        choices=MUNICIPALITY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'municipality-select'})
    )
    
    address_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe exact location: street name, building number, landmark...'
        }),
        help_text="GPS can be inaccurate. Please describe the location in detail."
    )
    
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+27 XX XXX XXXX',
            'type': 'tel'
        })
    )

    class Meta:
        model = Report
        fields = ['category', 'province', 'municipality', 'address_description', 
                  'description', 'photo', 'reported_language', 'phone_number']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'reported_language': forms.Select(attrs={'class': 'form-control'}),
        }