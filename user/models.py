from django.db import models

# Create your models here.


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, verbose_name='用户名', unique=True)
    email = models.EmailField(verbose_name='邮箱地址')
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    bio = models.TextField(verbose_name='个人简介', blank=True, null=True)
    
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        db_table = 'user_info'
        
    def __str__(self):
        return self.username
