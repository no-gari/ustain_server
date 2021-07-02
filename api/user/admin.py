from django.contrib import admin

from api.user.models import User, EmailVerifier, PhoneVerifier, Social


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailVerifier)
class EmailVerifierAdmin(admin.ModelAdmin):
    pass


@admin.register(PhoneVerifier)
class PhoneVerifierAdmin(admin.ModelAdmin):
    pass

