from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = u'Профиль'
    verbose_name_plural = u'Профиль'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'last_name', 'first_name', 'get_groups', 'get_branches', 'get_mobile', 'is_active')
    list_filter = ('is_active', 'groups')
    search_fields = ['last_name', 'profile.branch_default']
    list_select_related = ('profile',)

    def get_groups(self, instance):
        list_groups = ''
        for group in instance.groups.all():
            if list_groups == '':
                list_groups = group.name
            else:
                list_groups = list_groups + ', ' + group.name
        return list_groups
    get_groups.short_description = u'Группы'

    def get_branches(self, instance):
        list_branches = ''
        for branch in instance.profile.branch.all():
            if list_branches == '':
                list_branches = branch.name
            else:
                list_branches = list_branches + ', ' + branch.name
        return list_branches
    get_branches.short_description = u'Филиалы'

    def get_mobile(self, instance):
        return instance.profile.mobile_version
    get_mobile.short_description = u'Мобильная версия'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)