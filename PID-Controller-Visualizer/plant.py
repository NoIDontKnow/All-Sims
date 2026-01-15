class FirstOrderPlant:
    def __init__(self, time_constant=1.0, gain=1.0, dt=0.1):
        self.tau = time_constant
        self.gain = gain
        self.dt = dt
        self.state = 0.0

    def step(self, u):
        x = self.state
        dx = (-x + self.gain*u) / self.tau
        x_new = x + dx*self.dt
        self.state = x_new
        return self.state
