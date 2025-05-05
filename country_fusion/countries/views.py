from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics, permissions, filters
from rest_framework.response import Response

from .models import Country
from .serializers import CountrySerializer, CountryListSerializer, CountryCreateSerializer


# Web Views
@login_required
def country_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        countries = Country.objects.filter(name__icontains=search_query)
    else:
        countries = Country.objects.all()
        
    context = {
        'countries': countries,
        'search_query': search_query
    }
    return render(request, 'countries/country_list.html', context)


@login_required
def country_detail(request, pk):
    country = get_object_or_404(Country, pk=pk)
    
    # Get countries in the same region
    regional_countries = Country.objects.filter(
        region=country.region
    ).exclude(pk=country.pk)
    
    context = {
        'country': country,
        'regional_countries': regional_countries,
        'languages': country.get_languages(),
        'timezone': country.get_timezone()
    }
    return render(request, 'countries/country_detail.html', context)


# API Views
class CountryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cca2', 'cca3', 'capital']
    ordering_fields = ['name', 'population', 'region']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CountryCreateSerializer
        return CountryListSerializer
    
    def get_queryset(self):
        return Country.objects.all()


class CountryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CountryRegionAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountryListSerializer
    
    def get_queryset(self):
        country = get_object_or_404(Country, pk=self.kwargs['pk'])
        return Country.objects.filter(region=country.region).exclude(pk=country.pk)


class CountryLanguageAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountryListSerializer
    
    def get_queryset(self):
        language = self.kwargs['language'].lower()
        queryset = Country.objects.all()
        
        # Filter countries by language
        filtered_countries = []
        for country in queryset:
            country_languages = country.get_languages()
            if any(lang.lower() == language for lang in country_languages):
                filtered_countries.append(country.id)
        
        return Country.objects.filter(id__in=filtered_countries)


class CountrySearchAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountryListSerializer
    
    def get_queryset(self):
        query = self.kwargs['query']
        return Country.objects.filter(
            Q(name__icontains=query) | 
            Q(common_name__icontains=query) |
            Q(cca2__icontains=query) |
            Q(cca3__icontains=query)
        )