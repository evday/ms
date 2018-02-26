import re
from datetime import datetime,timedelta

from rest_framework import serializers
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
