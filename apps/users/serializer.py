import re
from datetime import datetime,timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self,mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile = mobile).count():
            raise serializers.ValidationError('用户名已存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError('手机号码不合法')

        #验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago,mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送不足60s')

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ("name","birthday","gender","email","mobile")

class UserRegSerializer(serializers.ModelSerializer):
    # 数据库中不存在的字段
    # write_only 只可写，不可以被序列化
    code = serializers.CharField(required=True,max_length=4,min_length=4,help_text='验证码',write_only=True,
                                 error_messages={
                                     "blank":"请输入验证码",
                                     "required":"请输入验证码",
                                     "max_length":"验证码错误",
                                     "min_length":"验证码错误",
                                 }
                                 )
    #UniqueValidar django rest-framework 提供的验证规则
    username = serializers.CharField(label='用户名',help_text='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户名已存在")])
    #这里password 设置write_only 是为了安全，不可被序列化返回,style 设置input框的样式，
    password = serializers.CharField(
        style={'input_type':'password'},help_text='密码',label='密码',write_only=True,
    )

    # 密文保存密码,接下来用django 的信号来实现

    # def create(self,validated_data):
    #     user = super().create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user




    def validate_code(self,code):
        '''
        验证验证码  局部钩子函数
        :param code:
        :return:
        '''
        # initial_data 存放着前端提交过来的数据
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_codes:
            # 最后一条记录
            last_record = verify_codes[0]
            #5分钟过期
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        '''
        全局钩子，attrs 是所有验证后返回后的总的字典
        :param attrs:
        :return:
        '''
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model=User
        fields=("username","code","mobile","password")
