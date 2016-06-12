from models import Light
from serializers import LightSerializer

from rest_framework import mixins
from rest_framework import generics

class LightList(mixins.ListModelMixin,
                generics.RetrieveUpdateAPIView):
    queryset = Light.objects.all()
    serializer_class = LightSerializer
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] is None:
            return self.list(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

