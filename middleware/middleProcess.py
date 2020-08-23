from django.http.response import JsonResponse, HttpResponse
from traceback import print_exc
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from django.conf import settings
from utils.common import Logger
logger = Logger().error


class SimpleMiddleware(RefreshJSONWebTokenSerializer):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code == 401:
            return JsonResponse({'code':401,'data':'会话失效'},status=401,json_dumps_params={'ensure_ascii':False})

        if request.headers.get('Authorization',None):
            try:
                token = self.validate({'token':request.headers['Authorization'].replace('JWT ','')})['token']
            except Exception as e:
                response.status_code = 401
            else:
                response.set_cookie('token',token,max_age=settings.JWT_EXPIRATION_DELTA)
        return response

    def process_exception(self,request,err):
        logger.exception(print_exc())
        return JsonResponse({"code":500,"msg":str(err)},status=500)

