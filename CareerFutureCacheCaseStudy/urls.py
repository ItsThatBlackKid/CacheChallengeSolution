"""CareerFutureCacheCaseStudy URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Case Study API')  # the api viewer to allow us to test the api.
urlpatterns = [
    path('api', schema_view),  # this.site.com/api
    path('message/', include('store.urls')),
    path('admin/', admin.site.urls),
]
