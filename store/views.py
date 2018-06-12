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


class DocumentViewSet(viewsets.ModelViewSet):
    """
    message -- The message in the document

    """

    lookup_field = 'id'
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, **kwargs):
        # serialize the received data
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():  # ensuring the data sent isn't malformed
            serialized.save()
            obj = Document.objects.all().latest('id')  # not a clean solution, but it works
            # caching the new document.
            cache.set('doc:'.format(obj.id), {"id": obj.id, "message": obj.message}, 30)

            return Response({"status": "Document created"}, status=status.HTTP_201_CREATED)

        return Response({
            "status": "Bad request",
            "message": "Could not create document with received data"
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        if 'doc:'.format(kwargs['id']) in cache:  # ensuring the requested document is still cached
            document = cache.get('doc:'.format(kwargs['id']))
            return Response(document, status=status.HTTP_200_OK)
        elif Document.objects.filter(id=kwargs['id']).exists():
            document = Document.objects.get(id=kwargs['id'])
            serialized = self.serializer_class(document)
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response({
            "status": "Failed Request",
            "message": "Resource not found"
        }, status=status.HTTP_404_NOT_FOUND)
