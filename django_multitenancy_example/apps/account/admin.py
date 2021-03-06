from django.contrib import admin
from django.contrib.auth import get_user_model
from tenant_users.permissions.models import UserTenantPermissions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain
from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()


@admin.register(UserTenantPermissions)
class PermAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_date']
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['created_date', '-id']
    filter_horizontal = ()


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant')
