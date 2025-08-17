from django.contrib import admin
from user.models import UserInfo

# Register your models here.
# 注册User模型到admin

from xsys.admin import XKModelAdmin


@admin.register(UserInfo)
class UserAdmin(XKModelAdmin):
    # 使用Django Admin原生属性替代自定义的xk_*属性
    list_display = ('username', 'email', 'age', 'is_active', "bio")
