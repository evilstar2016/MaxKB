# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： system_management.py
    @date：2024/3/19 13:47
    @desc: 邮箱管理
"""

from django.db import models

from common.mixins.app_model_mixin import AppModelMixin


class SettingType(models.IntegerChoices):
    """系统设置类型"""
    EMAIL = 0, '邮箱'

    RSA = 1, "私钥秘钥"


class SystemSetting(AppModelMixin):
    """
     系统设置
    """
    type = models.IntegerField(primary_key=True, verbose_name='设置类型', choices=SettingType.choices,
                               default=SettingType.EMAIL)

    meta = models.JSONField(verbose_name="配置数据", default=dict)

    class Meta:
        db_table = "system_setting"


class SystemDisplaySetting(models.Model):
    """系统外观设置模型"""

    # Logo设置
    header_logo = models.FileField(upload_to='logos/header/', null=True, blank=True, verbose_name='网站Logo')
    login_logo = models.FileField(upload_to='logos/login/', null=True, blank=True, verbose_name='登录Logo')
    favicon = models.FileField(upload_to='logos/favicon/', null=True, blank=True, verbose_name='网站图标')

    # 基础信息
    site_title = models.CharField(max_length=100, default='MaxKB', verbose_name='网站标题')
    site_slogan = models.CharField(max_length=200, blank=True, verbose_name='网站口号')

    # 主题配色
    theme_color = models.CharField(max_length=7, default='#3370FF', verbose_name='主题色')
    primary_color = models.CharField(max_length=7, default='#3370FF', verbose_name='主色调')
    secondary_color = models.CharField(max_length=7, default='#6B7280', verbose_name='辅助色')
    accent_color = models.CharField(max_length=7, default='#10B981', verbose_name='强调色')

    # 高级配置
    color_scheme = models.JSONField(default=dict, blank=True, verbose_name='配色方案')
    brand_elements = models.JSONField(default=dict, blank=True, verbose_name='品牌元素')
    custom_css = models.TextField(blank=True, verbose_name='自定义CSS')

    # 登录页配置
    login_background = models.FileField(upload_to='backgrounds/', null=True, blank=True, verbose_name='登录背景')
    login_layout = models.CharField(
        max_length=20,
        choices=[('left', '左侧'), ('center', '居中'), ('right', '右侧')],
        default='center',
        verbose_name='登录布局'
    )

    # 功能开关
    enable_dark_mode = models.BooleanField(default=False, verbose_name='启用暗色模式')
    show_brand_name = models.BooleanField(default=True, verbose_name='显示品牌名称')

    # 平台设置
    show_user_manual = models.BooleanField(default=True, verbose_name='显示用户手册')
    user_manual_url = models.URLField(blank=True, verbose_name='用户手册链接')
    show_forum = models.BooleanField(default=True, verbose_name='显示论坛')
    forum_url = models.URLField(blank=True, verbose_name='论坛链接')
    show_project = models.BooleanField(default=True, verbose_name='显示项目')
    project_url = models.URLField(blank=True, verbose_name='项目链接')

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_display_setting'
        verbose_name = '系统外观设置'
        verbose_name_plural = '系统外观设置'

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': getattr(self, 'id', None),
            'theme': self.theme_color,  # 兼容原有字段
            'icon': self.header_logo.url if self.header_logo else '',  # 兼容原有字段
            'header_logo': self.header_logo.url if self.header_logo else '',
            'login_logo': self.login_logo.url if self.login_logo else '',
            'favicon': self.favicon.url if self.favicon else '',
            'title': self.site_title,
            'slogan': self.site_slogan,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'accent_color': self.accent_color,
            'color_scheme': self.color_scheme or {
                'primary': self.primary_color,
                'secondary': self.secondary_color,
                'accent': self.accent_color
            },
            'brand_elements': self.brand_elements or {
                'show_brand_name': self.show_brand_name,
                'brand_position': 'left',
                'logo_size': 'medium'
            },
            'custom_css': self.custom_css,
            'login_image': self.login_background.url if self.login_background else '',  # 兼容原有字段
            'login_layout': self.login_layout,
            'enable_dark_mode': self.enable_dark_mode,
            'show_brand_name': self.show_brand_name,
            'show_user_manual': self.show_user_manual,
            'user_manual_url': self.user_manual_url,
            'show_forum': self.show_forum,
            'forum_url': self.forum_url,
            'show_project': self.show_project,
            'project_url': self.project_url,
            'showUserManual': self.show_user_manual,  # 兼容前端字段
            'userManualUrl': self.user_manual_url,
            'showForum': self.show_forum,
            'forumUrl': self.forum_url,
            'showProject': self.show_project,
            'projectUrl': self.project_url,
        }

    @classmethod
    def get_setting(cls):
        """获取设置，如果不存在则创建默认设置"""
        setting = cls.objects.first()
        if not setting:
            setting = cls.objects.create()
        return setting
