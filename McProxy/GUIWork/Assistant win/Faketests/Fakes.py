#test class begin::

class FakeClientConn():
    def __init__(self):
        self.time = 0

    def set(self, mode, arg, port=0):
        pass

    def connect(self):
        pass

    def check(self):
        self.time += 1
        if self.time > 15:
            return "success"
        else:
            return "connecting"

class FakeLib():
    def __init__(self):
        pass

    def summon_local_info(self):
        return "LALALALALALLSAJFOIUAWJFLIKAHSOIDafs"



#test class end::
