import requests
import json
from django.core.management.base import BaseCommand
from countries.models import Country


class Command(BaseCommand):
    help = 'Fetch countries data from the REST Countries API'

    def handle(self, *args, **options):
        url = 'https://restcountries.com/v3.1/all'
        self.stdout.write(self.style.SUCCESS(f'Fetching countries from {url}'))
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Clear existing countries
            if Country.objects.exists():
                self.stdout.write(self.style.WARNING('Clearing existing countries...'))
                Country.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS(f'Found {len(data)} countries'))
            count = 0
            
            for country_data in data:
                try:
                    # Extract required fields
                    name = country_data['name']['official']
                    common_name = country_data['name']['common']
                    cca2 = country_data['cca2']
                    cca3 = country_data['cca3']
                    
                    # Handle optional fields with defaults
                    capital = country_data.get('capital', [None])[0] if 'capital' in country_data else None
                    region = country_data.get('region', '')
                    subregion = country_data.get('subregion', '')
                    population = country_data.get('population', 0)
                    
                    # Get flag information
                    flag_url = country_data.get('flags', {}).get('png', '')
                    flag_emoji = country_data.get('flag', '')
                    
                    # Get timezones and languages
                    timezones = country_data.get('timezones', [])
                    languages = country_data.get('languages', {})
                    
                    # Create country object
                    Country.objects.create(
                        name=name,
                        common_name=common_name,
                        cca2=cca2,
                        cca3=cca3,
                        capital=capital,
                        region=region,
                        subregion=subregion,
                        population=population,
                        flag_url=flag_url,
                        flag_emoji=flag_emoji,
                        timezones=timezones,
                        languages=languages
                    )
                    count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing country {country_data.get("name", {}).get("common", "Unknown")}: {str(e)}')
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} countries'))
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching countries: {str(e)}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON response from API'))