from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ReviewList,ReviewDetail,ModelList,ModelDetail

urlpatterns = [
    path('review/',ReviewList.as_view()),
    path('review/<int:pk>',ReviewDetail.as_view()),
    path('model/',ModelList.as_view()),
    path('model/<int:pk>',ModelDetail.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)
