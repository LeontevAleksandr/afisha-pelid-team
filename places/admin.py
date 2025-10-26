from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Place, Image
from django.utils.html import mark_safe


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'preview', 'position')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;"/>')
        return ''
    preview.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'lat', 'lng')
    search_fields = ('title',)
    inlines = [ImageInline]