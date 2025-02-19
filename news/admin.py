from django.contrib import admin

from .models import Article, Category, Tag


admin.site.site_header = "My Blog Admin"
admin.site.site_title = "My Blog Admin Portal"
admin.site.index_title = "Welcome to My Blog Admin Portal"

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
