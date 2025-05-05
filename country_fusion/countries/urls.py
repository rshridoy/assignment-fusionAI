from django.urls import path
from . import views

urlpatterns = [
    # Web interface URLs
    path('', views.country_list, name='country_list'),
    path('countries/<int:pk>/', views.country_detail, name='country_detail'),
    
    # API URLs
    path('api/countries/', views.CountryListCreateAPIView.as_view(), name='api_country_list'),
    path('api/countries/<int:pk>/', views.CountryRetrieveUpdateDestroyAPIView.as_view(), name='api_country_detail'),
    path('api/countries/<int:pk>/region/', views.CountryRegionAPIView.as_view(), name='api_country_region'),
    path('api/countries/language/<str:language>/', views.CountryLanguageAPIView.as_view(), name='api_country_language'),
    path('api/countries/search/<str:query>/', views.CountrySearchAPIView.as_view(), name='api_country_search'),
]