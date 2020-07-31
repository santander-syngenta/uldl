import django_filters
from .models import *
from django_filters import CharFilter

class Presentationfilter(django_filters.FilterSet):

	class Meta:
		model = Presentation 
		fields = '__all__'
		exclude = ['pptx']