import numpy as np
import sijax

class BaseResponse(sijax.response.BaseResponse):

    def __init__(self,*args,**kwargs):
        sijax.response.BaseResponse.__init__(self,*args,**kwargs)

    def timeout(self,callback,timeout):
        self.call("window.visujax.timeout_sijax",[callback,timeout])

    def update_data(self,**kwargs):
        data = {}
        for name, value in kwargs.iteritems():
            if isinstance(value,np.ndarray):
                data[name] = value.tolist()
            else:
                data[name] = value
        self.call('window.visujax.UpdateData',[data])

