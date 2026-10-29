from django.contrib import admin
from django.db import models
from core.base_admin import BaseTabularInline, BaseModelAdmin
from core.models import Skill, SkillCategory, City, Region, Country
from django import forms




class RegionInline(BaseTabularInline):
    model = Region
    extra = 1
    fields = ('name', 'code')
    can_delete = True
    show_change_link = True

class CityInline(BaseTabularInline):
    model = City
    extra = 1
    can_delete = True
    show_change_link = True

@admin.register(Country)
class CountryAdmin(BaseModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)
    inlines = [RegionInline] # دمج المناطق داخل الدولة

@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',)
    search_fields = ('name',)
    inlines = [CityInline]

@admin.register(City)
class CityAdmin(BaseModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region__country', 'region')
    search_fields = ('name',)



class SkillInline(BaseTabularInline):
    model = Skill
    extra = 1
    fields = ('name',)


@admin.register(SkillCategory)
class SkillCategoryAdmin(BaseModelAdmin):
    list_display = ('name','icon')
    search_fields = ('name',)
    inlines = [SkillInline]  #


@admin.register(Skill)
class SkillAdmin(BaseModelAdmin):
    list_display = ('name','category','is_verified')
        
    search_fields = ('name',)
    list_filter = ('category','is_verified')
