from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.

class NewUser(AbstractUser):
    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]

    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, auto_now=True)
    code = models.UUIDField(verbose_name='uuid', default=uuid.uuid4, editable=False)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        pass


class Books(models.Model):
    name = models.CharField(verbose_name='书名', max_length=10)
    auther = models.CharField(verbose_name='作者', max_length=10)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        verbose_name_plural = '图书'


class Student(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=10)
    is_finished = models.BooleanField(verbose_name='是否毕业', default=False)
    student_info = models.OneToOneField(verbose_name='学生信息', to='StudentInfo', on_delete=models.CASCADE, null=True,
                                        blank=True)
    class_name = models.ForeignKey(verbose_name='班级', to='ClassName', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "学生"

    def __str__(self):
        return str(self.id) + '--' + self.name


class StudentInfo(models.Model):
    address = models.CharField(verbose_name='地址', max_length=10)

    class Meta:
        verbose_name_plural = "学生信息"

    def __str__(self):
        return str(self.id) + '--' + self.address


class ClassName(models.Model):
    name = models.CharField(verbose_name='班级名称', max_length=10)

    class Meta:
        verbose_name_plural = '班级'

    def __str__(self):
        return str(self.id) + '--' + self.name


class Teacher(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=10)
    student = models.ManyToManyField(verbose_name='学生', to='Student', blank=True)

    class Meta:
        verbose_name_plural = '老师'

    def __str__(self):
        return str(self.id) + '--' + self.name
