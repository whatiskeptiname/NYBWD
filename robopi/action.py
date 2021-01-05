import time as IO #just to start the server rpy.gpio not being installed



ma0 = 18
ma1 = 23
mb0 = 24
mb1 = 25
pwm_a = 26
pwm_b = 27

class Action:
    def __ini__(self):
        IO.setwarnings(False)
        IO.setmode(IO.BCM)

        IO.setup(ma0, IO.OUT)
        IO.setup(ma1, IO.OUT)
        IO.setup(mb0, IO.OUT)
        IO.setup(mb1, IO.OUT)
        IO.setup(pwm_a, IO.OUT)
        IO.setup(pwm_b, IO.OUT)

        IO.output(ma0 , 0)
        IO.output(ma1 , 0)
        IO.output(mb0, 0)
        IO.output(mb1, 0)
        IO.output(pwm_a, 0)
        IO.output(pwm_b, 0)

    def left(self, speed):
        IO.output(ma0 , 1)
        IO.output(ma1 , 0)
        IO.output(mb0, 1)
        IO.output(mb1, 0)
        pa = IO.PWM(pwm_a, 100)
        pb = IO.PWM(pwm_b, 100)
        pa.start(speed)
        pb.start(speed)

    def forward(self, speed):
        IO.output(ma0 , 0)
        IO.output(ma1 , 1)
        IO.output(mb0, 1)
        IO.output(mb1, 0)
        pa = IO.PWM(pwm_a, 100)
        pb = IO.PWM(pwm_b, 100)
        pa.start(speed)
        pb.start(speed)

    def right(self, speed):
        IO.output(ma0 , 0)
        IO.output(ma1 , 1)
        IO.output(mb0, 0)
        IO.output(mb1, 1)
        pa = IO.PWM(pwm_a, 100)
        pb = IO.PWM(pwm_b, 100)
        pa.start(speed)
        pb.start(speed)

    def backward(self, speed):
        IO.output(ma0 , 1)
        IO.output(ma1 , 0)
        IO.output(mb0, 0)
        IO.output(mb1, 1)
        pa = IO.PWM(pwm_a, 100)
        pb = IO.PWM(pwm_b, 100)
        pa.start(speed)
        pb.start(speed)

    def stop(self):
        IO.output(ma0 , 0)
        IO.output(ma1 , 0)
        IO.output(mb0, 0)
        IO.output(mb1, 0)
        pa = IO.PWM(pwm_a, 0)
        pb = IO.PWM(pwm_b, 0)
        pa.start(0)
        pb.start(0)