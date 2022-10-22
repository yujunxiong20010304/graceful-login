from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from oAuth.models import NewUser, Student, StudentInfo, ClassName, Teacher


# Register your models here.

class NewUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'roles')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    list_display = ('id', 'username', 'roles', 'email', 'is_active', 'last_login', 'code')
    list_display_links = ('id', 'username', 'roles', 'email', 'last_login')
    search_fields = ('username', 'email')


admin.site.register(NewUser, NewUserAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'student_info', 'class_name', 'is_finished')
    list_display_links = ('id', 'name', 'student_info', 'class_name', 'is_finished')


admin.site.register(Student, StudentAdmin)


class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    list_display_links = ('id', 'address')


admin.site.register(StudentInfo, StudentInfoAdmin)


class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(ClassName, ClassNameAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Teacher, TeacherAdmin)
