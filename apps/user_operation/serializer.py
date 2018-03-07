from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from .models import UserFav,UserLeavingMessage,UserAddress
from goods.serializer import GoodsSerialize


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerialize()
    class Meta:
        model = UserFav
        fields = ("goods","id")


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


class LeaveMessageSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户对象
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time =serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")
    class Meta:
        model = UserLeavingMessage

        fields = ("user", "message_type","subject","message","file","add_time", "id",)


class AddressSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户对象
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time =serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")
    class Meta:
        model = UserAddress

        fields = ("user", "province","city","district","address","add_time", "id","signer_name","signer_mobile")
