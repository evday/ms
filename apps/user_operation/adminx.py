import xadmin

from .models import UserFav,UserLeavingMessage,UserAddress

class UserFavAdmin(object):
    list_display = ['user','goods','add_time']

class UserLeavingMessageAdmin(object):
    list_display = ['user','message_type','message','add_time']

class UserAddressAdmin(object):
    list_display = ['single_name','single_mobile','district','address']

xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserLeavingMessage,UserLeavingMessageAdmin)
xadmin.site.register(UserAddress,UserAddressAdmin)