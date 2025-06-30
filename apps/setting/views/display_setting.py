from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io
import time
import json
from ..models import SystemDisplaySetting
from common.mixins.auth_mixins import AuthMixin
from common.response import Result


class DisplaySettingView(AuthMixin, APIView):
    """外观设置API视图"""
    
    def get(self, request):
        """获取外观设置"""
        try:
            setting = SystemDisplaySetting.get_setting()
            return Response(Result.success(setting.to_dict()))
        except Exception as e:
            return Response(
                Result.error(f'获取外观设置失败: {str(e)}'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """更新外观设置"""
        try:
            setting = SystemDisplaySetting.get_setting()
            data = request.data
            
            # 处理文件上传
            if 'header_logo' in request.FILES:
                if setting.header_logo:
                    setting.header_logo.delete(save=False)
                setting.header_logo = self._process_logo(
                    request.FILES['header_logo'], 
                    'header'
                )
            elif 'icon' in request.FILES:  # 兼容原有字段
                if setting.header_logo:
                    setting.header_logo.delete(save=False)
                setting.header_logo = self._process_logo(
                    request.FILES['icon'], 
                    'header'
                )
            
            if 'login_logo' in request.FILES:
                if setting.login_logo:
                    setting.login_logo.delete(save=False)
                setting.login_logo = self._process_logo(
                    request.FILES['login_logo'], 
                    'login'
                )
                
            if 'loginLogo' in request.FILES:  # 兼容前端字段
                if setting.login_logo:
                    setting.login_logo.delete(save=False)
                setting.login_logo = self._process_logo(
                    request.FILES['loginLogo'], 
                    'login'
                )
            
            if 'favicon' in request.FILES:
                if setting.favicon:
                    setting.favicon.delete(save=False)
                setting.favicon = self._process_favicon(
                    request.FILES['favicon']
                )
                
            if 'login_background' in request.FILES:
                if setting.login_background:
                    setting.login_background.delete(save=False)
                setting.login_background = self._process_background(
                    request.FILES['login_background']
                )
            elif 'loginImage' in request.FILES:  # 兼容前端字段
                if setting.login_background:
                    setting.login_background.delete(save=False)
                setting.login_background = self._process_background(
                    request.FILES['loginImage']
                )
            
            # 更新基础配置
            setting.site_title = data.get('title', data.get('site_title', setting.site_title))
            setting.site_slogan = data.get('slogan', data.get('site_slogan', setting.site_slogan))
            
            # 更新主题色（兼容原有字段）
            theme_color = data.get('theme', data.get('theme_color', setting.theme_color))
            setting.theme_color = theme_color
            setting.primary_color = data.get('primary_color', theme_color)
            
            # 更新配色方案
            setting.secondary_color = data.get('secondary_color', setting.secondary_color)
            setting.accent_color = data.get('accent_color', setting.accent_color)
            
            # 处理配色方案JSON
            color_scheme = data.get('color_scheme')
            if color_scheme:
                if isinstance(color_scheme, str):
                    color_scheme = json.loads(color_scheme)
                setting.color_scheme = color_scheme
                if 'primary' in color_scheme:
                    setting.primary_color = color_scheme['primary']
                    setting.theme_color = color_scheme['primary']
                if 'secondary' in color_scheme:
                    setting.secondary_color = color_scheme['secondary']
                if 'accent' in color_scheme:
                    setting.accent_color = color_scheme['accent']
            
            # 处理品牌元素JSON
            brand_elements = data.get('brand_elements')
            if brand_elements:
                if isinstance(brand_elements, str):
                    brand_elements = json.loads(brand_elements)
                setting.brand_elements = brand_elements
                if 'show_brand_name' in brand_elements:
                    setting.show_brand_name = brand_elements['show_brand_name']
            
            # 更新其他配置
            setting.custom_css = data.get('custom_css', setting.custom_css)
            setting.enable_dark_mode = data.get('enable_dark_mode', setting.enable_dark_mode)
            
            # 更新平台设置（兼容前端字段）
            setting.show_user_manual = data.get('showUserManual', data.get('show_user_manual', setting.show_user_manual))
            setting.user_manual_url = data.get('userManualUrl', data.get('user_manual_url', setting.user_manual_url))
            setting.show_forum = data.get('showForum', data.get('show_forum', setting.show_forum))
            setting.forum_url = data.get('forumUrl', data.get('forum_url', setting.forum_url))
            setting.show_project = data.get('showProject', data.get('show_project', setting.show_project))
            setting.project_url = data.get('projectUrl', data.get('project_url', setting.project_url))
            
            setting.save()
            
            return Response(Result.success(setting.to_dict()))
            
        except Exception as e:
            return Response(
                Result.error(f'更新外观设置失败: {str(e)}'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _process_logo(self, file, logo_type):
        """处理Logo文件"""
        try:
            img = Image.open(file)
            
            # 根据类型设置尺寸
            size_map = {
                'header': (200, 50),
                'login': (300, 80),
            }
            
            if logo_type in size_map:
                # 保持比例缩放
                img.thumbnail(size_map[logo_type], Image.Resampling.LANCZOS)
            
            # 保存处理后的图片
            output = io.BytesIO()
            
            # 如果是PNG，保持透明度
            if img.mode in ('RGBA', 'LA'):
                img.save(output, format='PNG', optimize=True)
                file_extension = 'png'
            else:
                # 转换为RGB并保存为JPEG
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output, format='JPEG', optimize=True, quality=85)
                file_extension = 'jpg'
            
            output.seek(0)
            
            file_name = f"{logo_type}_logo_{int(time.time())}.{file_extension}"
            path = f"logos/{logo_type}/{file_name}"
            
            return default_storage.save(path, ContentFile(output.read()))
            
        except Exception as e:
            raise Exception(f"处理{logo_type} Logo失败: {str(e)}")
    
    def _process_favicon(self, file):
        """处理Favicon"""
        try:
            img = Image.open(file)
            
            # Favicon固定为32x32
            img = img.resize((32, 32), Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            
            # 保存为PNG格式（浏览器兼容性更好）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(output, format='PNG', optimize=True)
            
            output.seek(0)
            
            file_name = f"favicon_{int(time.time())}.png"
            path = f"logos/favicon/{file_name}"
            
            return default_storage.save(path, ContentFile(output.read()))
            
        except Exception as e:
            raise Exception(f"处理Favicon失败: {str(e)}")
    
    def _process_background(self, file):
        """处理背景图片"""
        try:
            img = Image.open(file)
            
            # 背景图限制最大尺寸
            max_size = (1920, 1080)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            
            # 保存为JPEG格式以减小文件大小
            if img.mode in ('RGBA', 'LA'):
                # 如果有透明度，先转换为RGB
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
                
            img.save(output, format='JPEG', optimize=True, quality=85)
            output.seek(0)
            
            file_name = f"background_{int(time.time())}.jpg"
            path = f"backgrounds/{file_name}"
            
            return default_storage.save(path, ContentFile(output.read()))
            
        except Exception as e:
            raise Exception(f"处理背景图片失败: {str(e)}")