from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'cca2', 'capital', 'region', 'population', 'flag_url')


class CountryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'common_name', 'cca2', 'cca3', 'capital', 'region', 
                  'subregion', 'population', 'flag_url', 'flag_emoji', 
                  'timezones', 'languages')
        
    def validate_cca2(self, value):
        """
        Check that the country code is unique
        """
        if Country.objects.filter(cca2=value).exists():
            raise serializers.ValidationError("Country with this code already exists")
        return value