import time

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

