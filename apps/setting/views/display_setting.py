from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io
import time
import json
from common.auth import TokenAuth, has_permissions
from common.constants.permission_constants import RoleConstants


class DisplaySettingView(APIView):
    """外观设置API视图"""
    
    def get(self, request):
        """获取外观设置 - 公开访问，不需要认证"""
        try:
            # 返回默认的主题设置
            default_settings = {
                'theme': '#3370FF',
                'icon': '/static/ui/MaxKB.gif',
                'loginLogo': '/static/ui/MaxKB.gif',
                'loginImage': '/static/ui/login-bg.jpg',
                'favicon': '/static/ui/favicon.ico',
                'title': 'MaxKB',
                'slogan': '基于大语言模型的知识库问答系统',
                'colorScheme': {
                    'primary': '#3370FF',
                    'secondary': '#6B7280',
                    'accent': '#10B981'
                },
                'brandElements': {
                    'showBrandName': True,
                    'brandPosition': 'left',
                    'logoSize': 'medium'
                },
                'customCSS': '',
                'enableDarkMode': False,
                'showUserManual': True,
                'userManualUrl': 'https://maxkb.cn/docs/',
                'showForum': True,
                'forumUrl': 'https://github.com/1panel-dev/MaxKB/discussions',
                'showProject': True,
                'projectUrl': 'https://github.com/1panel-dev/MaxKB'
            }
            return Response({
                'code': 200,
                'message': 'success',
                'data': default_settings
            })
        except Exception as e:
            return Response(
                {'code': 500, 'message': f'获取外观设置失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DisplaySettingUpdateView(APIView):
    """外观设置更新API视图 - 需要管理员权限"""
    authentication_classes = [TokenAuth]
    
    @has_permissions(RoleConstants.ADMIN)
    def post(self, request):
        """更新外观设置"""
        try:
            data = request.data
            
            # 简化的主题更新逻辑，只保存基本配置
            updated_settings = {
                'theme': data.get('theme', '#3370FF'),
                'title': data.get('title', 'MaxKB'),
                'slogan': data.get('slogan', '基于大语言模型的知识库问答系统'),
                'colorScheme': data.get('colorScheme', {
                    'primary': '#3370FF',
                    'secondary': '#6B7280',
                    'accent': '#10B981'
                }),
                'showUserManual': data.get('showUserManual', True),
                'userManualUrl': data.get('userManualUrl', 'https://maxkb.cn/docs/'),
                'showForum': data.get('showForum', True),
                'forumUrl': data.get('forumUrl', 'https://github.com/1panel-dev/MaxKB/discussions'),
                'showProject': data.get('showProject', True),
                'projectUrl': data.get('projectUrl', 'https://github.com/1panel-dev/MaxKB')
            }
            
            return Response({
                'code': 200,
                'message': 'success',
                'data': updated_settings
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
    
    