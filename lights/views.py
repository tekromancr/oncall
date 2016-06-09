from django.shortcuts import render
from django.views.generic import TemplateView
from lights.models import Light
# Create your views here.
class LightBoardView(TemplateView):
    http_method_names = [u'get']
    template_name = 'lightboard.html'

    def get_context_data(self, **kwargs):
        kwargs['lights'] = Light.objects.all()
        return kwargs
