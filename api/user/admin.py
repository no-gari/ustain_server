from api.user.models import User, EmailVerifier, PhoneVerifier, UserGroup
from django.contrib import admin
from django import forms


@admin.register(UserGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    pass


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'name', 'email', 'profile_article', 'groups', 'birthday', 'categories', 'sex_choices')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('phone', 'name')


@admin.register(EmailVerifier)
class EmailVerifierAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneVerifier)
class PhoneVerifierAdmin(admin.ModelAdmin):
    pass
