import time

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings

class BaseViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            resp = super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response(ResDict(400,msg=str(e)))
        return Response(ResDict(200, data=resp.data))

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(ResDict(400, msg=str(e)))
        else:
            return Response(ResDict(200, msg='删除成功'))

    def list(self, request,*args, **kwargs):
        try:
            resp = super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(ResDict(400, msg=str(e)))
        else:
            return Response(ResDict(200, data=resp.data), status=resp.status_code)

    def create(self, request, *args,serializer=None, **kwargs):
        serializer_class = serializer or self.serializer_class
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(ResDict(400, msg=str(e)))
            return Response(ResDict(200,data=serializer.data, msg='添加成功'))

        return Response(ResDict(400, msg=hander_error(serializer.errors)))

    def update(self, request, *args,serializer=None,**kwargs):
        serializer_class = serializer or self.serializer_class
        obj = self.get_object()
        serializer = serializer_class(instance=obj,data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(ResDict(400, msg=str(e)))
            return Response(ResDict(200, msg='更新成功'))

        return Response(ResDict(400, msg=hander_error(serializer.errors)))


def get_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

def record(job_names=None):
    def hander(func):
        def _func(*args,**kwargs):
            st = time.time()
            result = func(*args,**kwargs)
            en = time.time() - st
            print(f"{job_names or func.__name__}用时:{en:.2f}s")
            return result

        return _func
    return hander

def hander_error(err):
    res = ''
    for i in err:
        if len(err[i])==1:
            res += err[i][0]
    return str(list(err.keys())[0]) + ':' + res

ResDict = lambda code=200,msg='',data='':{'code':code,"data":data,'msg':msg}

