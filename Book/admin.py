from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin
from Book.models import Category, Book, Images, Comment

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

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'book', 'user', 'status']
    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # add cumulative product count
        qs = Category.objects.add_related_count(qs, Book, 'category', 'products_cumulative_count', cumulative=True)
        # add none cumulative product count
        qs = Category.objects.add_related_count(qs, Book, 'category', 'products_count', cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'






admin.site.register(Category, CategoryAdmin2)
admin.site.register(Book, BookAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)