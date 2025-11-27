from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    bagian_choices = [
        ('kepala_desa', 'Kepala Desa'),
        ('sekretaris', 'Sekretaris Desa'),
        ('kaur_keuangan', 'Kaur Keuangan'),
        ('kaur_pembangunan', 'Kaur Pembangunan'),
        ('kaur_pemerintahan', 'Kaur Pemerintahan'),
        ('kaur_kesejahteraan', 'Kaur Kesejahteraan'),
        ('umum', 'Umum'),
    ]

    bagian = forms.ChoiceField(choices=bagian_choices, required=False)

    class Meta:
        model = ContactMessage
        fields = ['nama', 'email', 'telepon', 'bagian', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Masukkan nama lengkap'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'telepon': forms.TextInput(attrs={'placeholder': '0812-3456-7890'}),
            'subjek': forms.TextInput(attrs={'placeholder': 'Subjek pesan'}),
            'pesan': forms.Textarea(attrs={'placeholder': 'Tuliskan pesan Anda di sini...', 'rows':6}),
        }


from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["nama", "nik", "alamat"]
