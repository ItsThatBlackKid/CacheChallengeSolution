# from django.utils import cache
from pprint import pprint

from django.conf import settings
from django.core.cache import cache, caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Document
from store.serializers import DocumentSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    message -- The message in the document

    """

    lookup_field = 'id'
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, **kwargs):
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():
            serialized.save()
            obj = Document.objects.all().latest('id')
            cache.set('doc:'.format(obj.id), {"id": obj.id, "message": obj.message}, 30)

            return Response({"status": "Document created"}, status=status.HTTP_201_CREATED)

        return Response({
            "status": "Bad request",
            "message": "Could not create document with received data"
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        print(kwargs['id'])
        if 'doc:'.format(kwargs['id']) in cache:
            documents = cache.get('doc:'.format(kwargs['id']))
            return Response({
                "document": documents
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "Failed Request",
            "message": "Resource not found"
        }, status=status.HTTP_404_NOT_FOUND)
