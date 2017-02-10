from django.contrib import admin
from rango.models import Category, Page,Question,UserProfile
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'url','category')
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
admin.site.register(Page, PageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Question)
admin.site.register(UserProfile)
