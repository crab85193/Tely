from django.contrib import admin
from .models.user import User
from .models.user_activate_tokens import UserActivateTokens
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models.notice import Notice, UserNotice
from .models.reservation import ReservationParent, ReservationChild

from .models.store import Store

class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('email', 'id', 'is_active', 'password')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('username',)}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
           'classes': ('wide',),
           'fields': ('email', 'password1', 'password2'),
        }),
    )


class UserActivateTokensAdmin(admin.ModelAdmin):
    list_display = ('token_id', 'user', 'activate_token', 'expired_at')


# Register your models here.
admin.site.register(User)
admin.site.register(UserActivateTokens)
admin.site.register(Notice)
admin.site.register(UserNotice)
admin.site.register(ReservationParent)
admin.site.register(ReservationChild)
admin.site.register(Store)
