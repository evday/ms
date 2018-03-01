from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):

    #获取当前登录的用户对象
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        # 重写联合为一验证规则
        validate =[
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user",'goods'),
                message="已收藏"
            )
        ]

        fields = ("user","goods","id")