from random import choice

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import authentication
from rest_framework import permissions

from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializer import SmsSerializer,UserRegSerializer,UserDetailSerializer
from utils.yunpian import YunPian
from MxShop.settings import APIKEY
from .models import VerifyCode

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return  user
        except Exception as e:
            return None

class SmsCodeViewSet(CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数随机验证码
        :return:
        """

        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code,mobile=mobile)

        #根据云片网API文档 0代表发送成功，其他code代表出错，
        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            },status = status.HTTP_400_BAD_REQUEST)

        else:
            #验证成功保存到数据库
            code_record = VerifyCode(code = code,mobile=mobile)
            code_record.save()
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''用户'''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication,)

    # 重写get_serializer_class 方法，动态配置序列化类
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    # 重写get_permissions 方法，动态配置验证类(注册是无需认证的)
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(),]
        if self.action == "create":
            return []
        return []


    # 将token返回回去，写到浏览器cookies中，实现注册完成后自动登录
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 根据user生成token
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 访问用户详情页面，比如说users/1
    def get_object(self):
        return self.request.user


    #这里需要取到用户对象,源码只是做了保存，没有返回
    def perform_create(self, serializer):
        return serializer.save()




