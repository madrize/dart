from django.contrib import admin
from models import Article,Tag

def activate(modeladmin,request,queryset):
    queryset.update(is_active=True)
activate.short_description = "Activate selected articles"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','is_active','date_created','author')
    list_filter = ('is_active','date_created')
    prepopulated_fields = {"slug": ("title",)}
    actions = [activate]

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag,TagAdmin)
admin.site.register(Article,ArticleAdmin)
