from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import Landlord, Hobby, Tenant


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'username', 'email', 'phone', 'date_joined')
    search_fields = ('first_name', 'middle_name', 'last_name', 'user__username', 'email',)
    fieldsets = (
        (None, {
            'fields': ('user_link',)
        }),
        ('Персональная информация', {
            'fields': ('avatar', 'username', 'password', 'first_name', 'middle_name',
                       'last_name', 'birth_date', 'email', 'phone', 'hobby')
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('avatar', 'username', 'password', 'first_name', 'middle_name', 'last_name',
                       'birth_date', 'email', 'phone', 'hobby'),
        }),
    )
    autocomplete_fields = ('hobby',)
    readonly_fields = ('user_link',)

    @admin.display(description='Дата регистрации')
    def date_joined(self, obj):
        return obj.user.date_joined

    @admin.display(description='Логин')
    def username(self, obj):
        return obj.user.username

    @admin.display(description='Пользователь')
    def user_link(self, obj):
        return mark_safe(f'<a href="{reverse("admin:auth_user_change", args=[obj.user_id])}">{obj.user}</a>')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Landlord)
class LandlordAdmin(ProfileAdmin):
    pass


@admin.register(Tenant)
class TenantAdmin(ProfileAdmin):
    pass
