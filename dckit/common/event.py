class Event(object):
    def __init__(self, name):
        self.__name = name
        self.__handlers = []
 
    def __add__(self, eventhandler):
        if not hasattr(eventhandler, '__call__'):
            raise TypeError("Method expected")
        self.__handlers.append(eventhandler)
        return self
 
    def __sub__(self, eventhandler):
        self.__handlers.remove(eventhandler)
        return self
 
    def __call__(self, args):
        self.trigger(args)
 
    def trigger(self, args):
        for handler in self.__handlers:
            handler(*args)


#class Event:
#    def init(self):
#        self.listeners = []
#    def call(self, params):
#        for l in self.listeners:
#            l(params)
#    def add(self, listener):
#        self.listeners.append(listener)
#        return self
#    def sub(self, listener):
#        self.listeners.remove(listener)
#        return self