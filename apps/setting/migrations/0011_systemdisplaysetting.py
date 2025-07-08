# Generated manually for SystemDisplaySetting

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0010_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemDisplaySetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_logo', models.FileField(blank=True, null=True, upload_to='logos/header/', verbose_name='网站Logo')),
                ('login_logo', models.FileField(blank=True, null=True, upload_to='logos/login/', verbose_name='登录Logo')),
                ('favicon', models.FileField(blank=True, null=True, upload_to='logos/favicon/', verbose_name='网站图标')),
                ('site_title', models.CharField(default='MaxKB', max_length=100, verbose_name='网站标题')),
                ('site_slogan', models.CharField(blank=True, max_length=200, verbose_name='网站口号')),
                ('theme_color', models.CharField(default='#3370FF', max_length=7, verbose_name='主题色')),
                ('primary_color', models.CharField(default='#3370FF', max_length=7, verbose_name='主色调')),
                ('secondary_color', models.CharField(default='#6B7280', max_length=7, verbose_name='辅助色')),
                ('accent_color', models.CharField(default='#10B981', max_length=7, verbose_name='强调色')),
                ('color_scheme', models.JSONField(blank=True, default=dict, verbose_name='配色方案')),
                ('brand_elements', models.JSONField(blank=True, default=dict, verbose_name='品牌元素')),
                ('custom_css', models.TextField(blank=True, verbose_name='自定义CSS')),
                ('login_background', models.FileField(blank=True, null=True, upload_to='backgrounds/', verbose_name='登录背景')),
                ('login_layout', models.CharField(choices=[('left', '左侧'), ('center', '居中'), ('right', '右侧')], default='center', max_length=20, verbose_name='登录布局')),
                ('enable_dark_mode', models.BooleanField(default=False, verbose_name='启用暗色模式')),
                ('show_brand_name', models.BooleanField(default=True, verbose_name='显示品牌名称')),
                ('show_user_manual', models.BooleanField(default=True, verbose_name='显示用户手册')),
                ('user_manual_url', models.URLField(blank=True, verbose_name='用户手册链接')),
                ('show_forum', models.BooleanField(default=True, verbose_name='显示论坛')),
                ('forum_url', models.URLField(blank=True, verbose_name='论坛链接')),
                ('show_project', models.BooleanField(default=True, verbose_name='显示项目')),
                ('project_url', models.URLField(blank=True, verbose_name='项目链接')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '系统外观设置',
                'verbose_name_plural': '系统外观设置',
                'db_table': 'system_display_setting',
            },
        ),
    ]