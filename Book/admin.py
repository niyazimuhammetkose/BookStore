from django.contrib import admin

# Register your models here.
from Book.models import Category, Book


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'publisher', 'price', 'amount', 'status']
    list_filter = ['title', 'author', 'category', 'publisher', 'status']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)