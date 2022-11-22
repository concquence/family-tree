from django.contrib import admin
from django.utils.safestring import mark_safe
from .utils import AdminMixin
from .models import Person, Image, Document


class PersonAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'gender', 'father', 'mother', 'partners', 'get_photo', 'tree_owner')
    list_display_links = ('id', 'first_name')
    search_fields = ('id', 'first_name', 'last_name', 'bio')
    fields = ('tree_owner', 'gender', 'first_name', 'last_name', 'maiden_name', 'birth', 'death',
              'lived_ca', 'father', 'mother', 'spouse', 'bio', 'photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'Нет фото'
    get_photo.short_description = "Миниатюра"
    save_on_top = True


class ImageAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('id', 'get_filename', 'get_persons', 'description')
    list_display_links = ('id', 'get_filename',)
    search_fields = ('id', 'description')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['description'].required = False
        return form


class DocumentAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('id', 'get_filename', 'get_document_owner', 'description')
    list_display_links = ('id', 'get_filename',)
    search_fields = ('id', 'description')


admin.site.register(Person, PersonAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Document, DocumentAdmin)
