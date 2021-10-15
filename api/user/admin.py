from api.user.models import User, EmailVerifier, PhoneVerifier, UserGroup, Categories
from api.commerce.customer.models import UserShipping, ShippingRequest
from django.contrib import admin
from django import forms


@admin.register(Categories)
class CategoryAdmiin(admin.ModelAdmin):
    pass


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


@admin.register(UserShipping)
class UserAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(ShippingRequest)
class ShippingRequestAdmin(admin.ModelAdmin):
    pass
