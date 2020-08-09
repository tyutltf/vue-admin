import time
from rest_framework_jwt.settings import api_settings

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



ResDict = lambda code=200,msg='',data='':{'code':code,"data":data,'msg':msg}

