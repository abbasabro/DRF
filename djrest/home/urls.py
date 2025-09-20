

from django.urls import path
from home.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product/v2', ProductViewSet, basename='products')



urlpatterns = [
    path ('', first_api),
    path('api/author/',AuthorApi.as_view()),
    path('api/author/v1/',AuthorApiV1.as_view()),
    path('api/author/v2/',AuthorMixin.as_view()),
    path ('create_records/', create_records),
    path ('view_records/', view_records),
    path ('update_records/', update_records),
    path ('delete_records/<id>/', delete_records),
    path ('create_book/', create_book),
    path ('view_book/', view_book),
    path ('create_user/', create_user),
    path ('api/v2/student/', StudentApi.as_view()),
    path ('api/v3/student/<int:pk>/', StudentApiMixix.as_view()),
    path ('api/product/', ProductListCreate.as_view()),
    path ('api/register/', RegisterApi.as_view()),
    path ('api/login/', LoginApi.as_view()),
]

urlpatterns += router.urls