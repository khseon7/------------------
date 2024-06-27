from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ModelList,ModelDetail

urlpatterns = [
    path('model/',ModelList.as_view()),
    path('model/<int:pk>',ModelDetail.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)
