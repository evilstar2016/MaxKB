from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io
import time
import json
from common.auth import TokenAuth, has_permissions
from common.constants.permission_constants import RoleConstants
from setting.models.system_management import SystemDisplaySetting


class DisplaySettingView(APIView):
    """外观设置API视图"""
    
    def get(self, request):
        """获取外观设置 - 公开访问，不需要认证"""
        try:
            # 从数据库获取设置
            setting = SystemDisplaySetting.get_setting()
            
            # 返回设置的字典格式
            return Response({
                'code': 200,
                'message': 'success',
                'data': setting.to_dict()
            })
        except Exception as e:
            return Response(
                {'code': 500, 'message': f'获取外观设置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class DisplaySettingUpdateView(APIView):
    """外观设置更新API视图 - 需要管理员权限"""
    authentication_classes = [TokenAuth]
    
    def post(self, request):
        """更新外观设置"""
        try:
            data = request.data
            files = request.FILES
            
            # 获取或创建设置实例
            setting = SystemDisplaySetting.get_setting()
            
            # 更新基本设置
            if 'theme' in data:
                setting.theme_color = data['theme']
                setting.primary_color = data['theme']  # 保持兼容性
            if 'title' in data:
                setting.site_title = data['title']
            if 'slogan' in data:
                setting.site_slogan = data['slogan']
            
            # 处理文件上传
            if 'icon' in files:
                setting.header_logo = files['icon']
            if 'loginLogo' in files:
                setting.login_logo = files['loginLogo']
            if 'favicon' in files:
                setting.favicon = files['favicon']
            if 'loginImage' in files:
                setting.login_background = files['loginImage']
            
            # 更新颜色方案 - 处理JSON字符串
            if 'colorScheme' in data:
                try:
                    if isinstance(data['colorScheme'], str):
                        color_scheme = json.loads(data['colorScheme'])
                    else:
                        color_scheme = data['colorScheme']
                    setting.color_scheme = color_scheme
                    if 'primary' in color_scheme:
                        setting.primary_color = color_scheme['primary']
                    if 'secondary' in color_scheme:
                        setting.secondary_color = color_scheme['secondary']
                    if 'accent' in color_scheme:
                        setting.accent_color = color_scheme['accent']
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # 更新品牌元素 - 处理JSON字符串
            if 'brandElements' in data:
                try:
                    if isinstance(data['brandElements'], str):
                        brand_elements = json.loads(data['brandElements'])
                    else:
                        brand_elements = data['brandElements']
                    setting.brand_elements = brand_elements
                    if 'showBrandName' in brand_elements:
                        setting.show_brand_name = brand_elements['showBrandName']
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # 更新功能开关
            if 'enableDarkMode' in data:
                setting.enable_dark_mode = str(data['enableDarkMode']).lower() == 'true'
            if 'showUserManual' in data:
                setting.show_user_manual = str(data['showUserManual']).lower() == 'true'
            if 'userManualUrl' in data:
                setting.user_manual_url = data['userManualUrl']
            if 'showForum' in data:
                setting.show_forum = str(data['showForum']).lower() == 'true'
            if 'forumUrl' in data:
                setting.forum_url = data['forumUrl']
            if 'showProject' in data:
                setting.show_project = str(data['showProject']).lower() == 'true'
            if 'projectUrl' in data:
                setting.project_url = data['projectUrl']
            
            # 更新自定义CSS
            if 'customCSS' in data:
                setting.custom_css = data['customCSS']
            
            # 保存到数据库
            setting.save()
            
            return Response({
                'code': 200,
                'message': 'success',
                'data': setting.to_dict()
            })
            
        except Exception as e:
            return Response(
                {'code': 500, 'message': f'更新外观设置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class AuthTypesView(APIView):
    """认证类型API视图 - 公开访问"""
    
    def get(self, request):
        """获取认证类型列表"""
        try:
            # 返回默认的认证类型配置，只支持基本的用户名密码登录
            auth_types = {
                'default': 'user',
                'types': ['user'],  # 只支持基本的用户登录
                'oauth': []  # 没有OAuth认证方式
            }
            return Response({
                'code': 200,
                'message': 'success', 
                'data': auth_types
            })
        except Exception as e:
            return Response(
                {'code': 500, 'message': f'获取认证类型失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QrTypeView(APIView):
    """二维码类型API视图 - 公开访问"""
    
    def get(self, request):
        """获取二维码类型配置"""
        try:
            # 返回默认的二维码配置，当前不支持二维码登录
            qr_config = {
                'enabled': False,
                'types': [],
                'message': '当前版本不支持二维码登录'
            }
            return Response({
                'code': 200,
                'message': 'success',
                'data': qr_config
            })
        except Exception as e:
            return Response(
                {'code': 500, 'message': f'获取二维码配置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    