from django.contrib import admin

from .models import Article, Category, Tag


admin.site.site_header = "My Blog Admin"
admin.site.site_title = "My Blog Admin Portal"
admin.site.index_title = "Welcome to My Blog Admin Portal"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'views')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
