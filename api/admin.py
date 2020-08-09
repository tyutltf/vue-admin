from django.contrib import admin
from django.contrib.auth.admin import UserAdmin,Group,GroupAdmin
from api.models import Book,User,Menu,MenuChild,Role
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
class showUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('telephone'),{'fields':('telephone','role')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    def get_groups(self,obj):
        return ''.join(list(obj.groups.all().values_list('name',flat=True)))

    list_display = ('username', 'email', 'is_staff','telephone','role','get_groups')
    list_per_page = 12
    list_editable = ('email','role')

class groupList(GroupAdmin):
    filter_horizontal = ('permissions','user')
    list_display = ('id','name')
    list_editable = ('name',)

class showMenu(admin.ModelAdmin):
    list_display = ('id','name')
    list_editable = ('name',)

class showRole(admin.ModelAdmin):
    list_display = ('id','name','create_date')
    list_editable = ('name',)

    # def save_form(self, request, form, change):
    #     obj = super(showRole, self).save_form(request,form,change)
    #     print(obj.groups.all())
    #     return obj



admin.site.unregister(Group)
admin.site.register(Group,groupList)
admin.site.register(User,showUser)
admin.site.register(Book)
admin.site.register(Role,showRole)
admin.site.register(Menu,showMenu)
admin.site.register(MenuChild,showMenu)
