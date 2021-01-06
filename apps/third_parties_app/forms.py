from django.forms import ModelForm

from .models import City

class CityForm(ModelForm):
    
    class Meta:
        model = City
        
        fields = ['city_name', 'city_id']
    
    