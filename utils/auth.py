# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from django.conf import settings
#
#
#
#
# class tokenAuth(JSONWebTokenAuthentication):
#
#     def authenticate(self, request):
#
#         method = settings.JWT_WHITE_LIST.get(request.path,None)
#         # self.per
#         if method.upper() == request.method:
#             # return super().authenticate(request)
#             pass
#
