from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,Group,GroupAdmin
from api.models import Book,User,Menu,MenuChild
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
class showUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('telephone'),{'fields':('telephone',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    def get_groups(self,obj):
        return ''.join(list(obj.groups.all().values_list('name',flat=True)))

    list_display = ('username', 'email', 'is_staff','telephone','get_groups')

class groupList(GroupAdmin):
    filter_horizontal = ('permissions','user')
admin.site.unregister(Group)
admin.site.register(Group,groupList)
admin.site.register(User,showUser)
admin.site.register(Book)
admin.site.register(Menu)
admin.site.register(MenuChild)
