from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'difficulty',
        'is_published',
        'is_featured',
        'created_at',
    )
    list_filter = ('category', 'difficulty', 'is_published', 'is_featured')
    search_fields = ('title', 'short_description', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}