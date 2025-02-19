from django.contrib import admin

from .models import Article, Category, Tag


admin.site.site_header = "My Blog Admin"
admin.site.site_title = "My Blog Admin Portal"
admin.site.index_title = "Welcome to My Blog Admin Portal"


class ArticleAdmin(admin.ModelAdmin):
    # list_display отображает поля в таблице
    list_display = ('title', 'category', 'publication_date', 'views')
    # list_filter позволяет фильтровать по полям
    list_filter = ('category',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
