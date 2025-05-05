from django.db import models
import json


class Country(models.Model):
    name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    cca2 = models.CharField(max_length=2, unique=True)
    cca3 = models.CharField(max_length=3)
    capital = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100, blank=True, null=True)
    population = models.BigIntegerField()
    flag_url = models.URLField(max_length=500)
    flag_emoji = models.CharField(max_length=10, blank=True, null=True)
    timezones = models.JSONField(default=list)
    languages = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_languages(self):
        """Returns the languages as a list"""
        if isinstance(self.languages, str):
            return list(json.loads(self.languages).values())
        return list(self.languages.values())

    def get_timezone(self):
        """Returns the first timezone"""
        if isinstance(self.timezones, str):
            timezones = json.loads(self.timezones)
        else:
            timezones = self.timezones
        
        if timezones and len(timezones) > 0:
            return timezones[0]
        return None