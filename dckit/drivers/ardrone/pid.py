#------------------------------------------------------------------------------
# PID.py
# A simple implementation of a PID controller
#------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#------------------------------------------------------------------------------

import time


class PID:
    """ Simple PID control.

        This class implements a simplistic PID control algorithm. When first
        instantiated all the gain variables are set to zero, so calling
        the method GenOut will just return zero.
    """
    def __init__(self, Kp=0, Kd=0, Ki=0):
        # initialze gains
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki

        self.Initialize()

    def SetKp(self, invar):
        """ Set proportional gain. """
        self.Kp = invar

    def SetKi(self, invar):
        """ Set integral gain. """
        self.Ki = invar

    def SetKd(self, invar):
        """ Set derivative gain. """
        self.Kd = invar

    def SetPrevErr(self, preverr):
        """ Set previous error value. """
        self.prev_err = preverr

    def Initialize(self):
        # initialize delta t variables
        self.currtm = time.time()
        self.prevtm = self.currtm

        self.prev_err = 0

        # term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def GenOut(self, error):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the error signal from a summing junction
            (the error parameter).
        """
        self.currtm = time.time()               # get t
        dt = self.currtm - self.prevtm          # get delta t
        de = error - self.prev_err              # get delta error

        self.Cp = self.Kp * error               # proportional term
        self.Ci += error * dt                   # integral term

        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de / dt                   # derivative term

        self.prevtm = self.currtm               # save t for next pass
        self.prev_err = error                   # save t-1 error

        # sum the terms and return the result
        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)

# class PID:

#     def __init__(self, P=1.0, I=0.0, D=10.0, Derivator=0, Integrator=0,
#                  Integrator_max=300, Integrator_min=-200, set_point=0.0,
#                  power=1.0):

#         self.Kp=P
#         self.Ki=I
#         self.Kd=D
#         self.Derivator=Derivator
#         self.power = power
#         self.Integrator=Integrator
#         self.Integrator_max=Integrator_max
#         self.Integrator_min=Integrator_min
#         self.last_error = 0.0
#         self.last_value = 0.0

#         self.set_point=set_point
#         self.error=0.0

#     def update(self,current_value):
#         """
#         Calculate PID output value for given reference input and feedback
#         """

#         self.error = self.set_point - current_value

#         self.P_value = self.Kp * self.error
#         if (self.last_value >= current_value):
#             change = self.error - self.last_error
#         else:
#             change = 0.0

#         if self.error > 0.0:
#             self.I_value = self.Integrator * self.Ki
#         else:
#             self.I_value = (self.Integrator * self.Ki)


#         #self.D_value = self.Kd * ( self.error - self.Derivator)
#         self.D_value = self.Kd * change
#         self.Derivator = self.error

#         self.Integrator = self.Integrator + self.error/200.0

#         if self.Integrator > self.Integrator_max:
#             self.Integrator = self.Integrator_max
#         elif self.Integrator < self.Integrator_min:
#             self.Integrator = self.Integrator_min

#         self.last_error = self.error
#         self.last_value = current_value

#         PID = self.P_value + self.I_value + self.D_value

#         return PID

#     def set_pointm(self,set_point):
#         """Initilize the setpoint of PID"""
#         self.set_point = set_point
#         self.Integrator=0
#         self.Derivator=0

# class PID_RP:

#     def __init__(self, P=1.0, I=0.0, D=10.0, Derivator=0, Integrator=0,
#                  Integrator_max=20000, Integrator_min=-20000, set_point=0.0,
#                  power=1.0):

#         self.Kp=P
#         self.Ki=I
#         self.Kd=D
#         self.Derivator=Derivator
#         self.power = power
#         self.Integrator=Integrator
#         self.Integrator_max=Integrator_max
#         self.Integrator_min=Integrator_min
#         self.last_error = 0.0
#         self.last_value = 0.0

#         self.set_point=set_point
#         self.error=0.0

#     def update(self,current_value):
#         """
#         Calculate PID output value for given reference input and feedback
#         """

#         self.error = self.set_point - current_value

#         self.P_value = self.Kp * self.error
#         change = self.error - self.last_error

#         self.I_value = self.Integrator * self.Ki

#         #self.D_value = self.Kd * ( self.error - self.Derivator)
#         self.D_value = self.Kd * change
#         self.Derivator = self.error

#         self.Integrator = self.Integrator + self.error

#         if self.Integrator > self.Integrator_max:
#             self.Integrator = self.Integrator_max
#         elif self.Integrator < self.Integrator_min:
#             self.Integrator = self.Integrator_min

#         self.last_error = self.error
#         self.last_value = current_value

#         PID = self.P_value + self.I_value + self.D_value

#         return PID

#     def set_pointm(self,set_point):
#         """
#         Initilize the setpoint of PID
#         """
#         self.set_point = set_point
#         self.Integrator=0
#         self.Derivator=0
