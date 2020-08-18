from django.contrib import admin

# Register your models here.
from Book.models import Category, Book, Images

class BookImageInLine(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'publisher', 'price', 'amount', 'image_tag', 'status']
    list_filter = ['title', 'author', 'category', 'publisher', 'status']
    inlines = [BookImageInLine]
    readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Images, ImagesAdmin)