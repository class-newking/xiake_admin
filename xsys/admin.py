from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest
from django.db import models


class XKModelAdmin(ModelAdmin):
    """
    自定义XKAdmin基类，继承自ModelAdmin
    提供基础的可扩展和定制化功能
    """

    # 列试页配置
    list_per_page = 20  # 每页显示数量
    list_max_show_all = 200  # 最大显示全部数量
    
    def __init__(self, model, admin_site):
        """
        初始化XKModelAdmin实例
        """
        super().__init__(model, admin_site)
    
    # 自定义字段显示
    def get_list_display(self, request):
        """
        动态获取列表显示字段
        子类可以重写此方法来根据用户权限等条件动态调整显示字段
        """
        return super().get_list_display(request)
    
    # 自定义查询集合
    def get_queryset(self, request):
        """
        自定义查询集合，可以用于添加默认过滤条件等
        """
        qs = super().get_queryset(request)
        return qs
    
    # 自定义表单字段
    def get_form(self, request, obj=None, **kwargs):
        """
        动态调整表单字段
        """
        form = super().get_form(request, obj, **kwargs)
        return form
    
    # 自定义是否可查看
    def has_view_permission(self, request, obj=None):
        """
        自定义查看权限
        """
        return super().has_view_permission(request, obj)
    
    # 自定义是否可添加
    def has_add_permission(self, request):
        """
        自定义添加权限
        """
        return super().has_add_permission(request)
    
    # 自定义是否可修改
    def has_change_permission(self, request, obj=None):
        """
        自定义修改权限
        """
        return super().has_change_permission(request, obj)
    
    # 自定义是否可删除
    def has_delete_permission(self, request, obj=None):
        """
        自定义删除权限
        """
        return super().has_delete_permission(request, obj)
    
    # 列表页操作
    def get_actions(self, request):
        """
        自定义批量操作
        """
        actions = super().get_actions(request)
        return actions
    
    # 保存前处理
    def save_model(self, request, obj, form, change):
        """
        保存模型前的处理逻辑
        """
        super().save_model(request, obj, form, change)
    
    # 删除前处理
    def delete_model(self, request, obj):
        """
        删除模型前的处理逻辑
        """
        super().delete_model(request, obj)
    
    # 批量删除
    def delete_queryset(self, request, queryset):
        """
        批量删除处理逻辑
        """
        super().delete_queryset(request, queryset)
        
    # 获取列表页显示的字段
    def get_list_display_links(self, request, list_display):
        """
        获取列表页中作为链接显示的字段
        """
        return super().get_list_display_links(request, list_display)
        
    # 获取搜索字段
    def get_search_results(self, request, queryset, search_term):
        """
        自定义搜索结果
        """
        return super().get_search_results(request, queryset, search_term)
        
    # 获取只读字段
    def get_readonly_fields(self, request, obj=None):
        """
        获取只读字段
        """
        return super().get_readonly_fields(request, obj)
        
    # 获取字段集
    def get_fieldsets(self, request, obj=None):
        """
        自定义字段集显示
        """
        return super().get_fieldsets(request, obj)
        
    # 获取列表过滤器
    def get_list_filter(self, request):
        """
        获取列表过滤器
        """
        return super().get_list_filter(request)

