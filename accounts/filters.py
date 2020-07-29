import django_filters
from .models import *
from django_filters import CharFilter

class Presentationfilter(django_filters.FilterSet):
	title = CharFilter(field_name='title', lookup_expr='icontains')

	class Meta:
		model = Presentation 
		fields = '__all__'
		exclude = ['pptx']