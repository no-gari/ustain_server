from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from django.db import transaction
import re
from . import models


def get_ipaddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for
    else:
        return request.META.get('REMOTE_ADDR')


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.Categories
        fields = ('title', 'mid', 'description', 'snapshot_image')

    def clean(self):
        r = re.compile(r'[^A-Za-z0-9]+')
        result = r.search(self.cleaned_data['mid'])
        if result is not None:
            self.add_error('mid', '영문+숫자만 가능합니다.')
            raise forms.ValidationError([])


@admin.register(models.Categories)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('get_id', 'title', 'mid', 'snapshot_image')
    list_display_links = ('title',)
    search_fields = ('title', 'mid',)

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'


class FilesInlineAdmin(admin.StackedInline):
    model = models.Files
    readonly_fields = ['file_image_small']

    def file_image_small(self, obj):
        if obj.org_file_name != '':
            file_ext = obj.org_file_name.split('.')[1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')

    file_image_small.short_description = '이미지'

    class Media:
        js = (
            'js/myscript.js',
        )


class MagazinesAdminForm(forms.ModelForm):
    class Meta:
        model = models.Magazines
        fields = ('categories', 'is_main', 'like_users', 'published', 'comments_banned', 'title', 'content', 'hits')

    def save(self, commit=True):
        try:
            self.instance.user = self.request.user
            self.instance.ipaddress = get_ipaddress(self.request)

            instance = super().save(commit=False)
            instance.save()

            content = self.cleaned_data['content']
            img_contents = re.findall(r'django-summernote/.*?"', content)
            for img in img_contents:
                imgs_path = img[0:len(img) - 1]
                summernote = models.Summernote.objects.get(file=imgs_path)
                summernote.document = instance
                summernote.save()
        except:
            instance = super().save(commit=False)

        return instance


@admin.register(models.Magazines)
class MagazinesAdmin(SummernoteModelAdmin):
    form = MagazinesAdminForm
    list_display = ('get_id', 'title', 'hits', 'get_likes')
    list_display_links = ('title',)
    list_filter = ['title']
    search_fields = ('title', 'user',)
    readonly_fields = ('hits',)
    summernote_fields = ('content',)
    inlines = (FilesInlineAdmin,)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'

    def get_likes(self, obj):
        try:
            instance = obj.like_users.count()
        except:
            instance = 0
        return instance

    get_likes.short_description = '좋아요 수'


@admin.register(models.MagazineComments)
class MagazineCommentsAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'content', 'user', 'magazines',)
    list_display_links = ('content',)
    readonly_fields = ('user',)
    list_filter = ['magazines']
    autocomplete_fields = ['magazines']

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'

    def save_model(self, request, obj, form, change):
        if obj.user_id is None:
            obj.user = request.user
        if obj.ipaddress is None:
            obj.ipaddress = get_ipaddress(request)
        return super().save_model(request, obj, form, change)


@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'magazines', 'file', 'org_file_name', 'created_at', 'updated_at',)
    list_display_links = ('magazines',)
    list_filter = ['magazines']
    search_fields = ('org_file_name',)
    readonly_fields = ['file_image_small']
    autocomplete_fields = ['magazines']

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'

    def file_image_small(self, obj):
        if obj.org_file_name != '':
            file_ext = obj.org_file_name.split('.')[1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')

    file_image_small.short_description = '이미지'


admin.site.unregister(models.Summernote)


@admin.register(models.Summernote)
class SummernoteAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'user', 'magazines', 'name', 'file', 'uploaded', 'ipaddress',)
    list_display_links = ('magazines', 'name',)
    readonly_fields = ['magazines', 'ipaddress', 'user', 'name', 'file_image_small']
    autocomplete_fields = ['magazines']

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'

    def has_add_permission(self, request):
        return False

    def file_image_small(self, obj):
        if obj.name != '':
            file_ext = obj.name.split('.')[1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')

    file_image_small.short_description = '이미지'


