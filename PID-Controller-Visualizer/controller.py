class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt=0.1, integrator_limit=None):
        self.kp = kp; self.ki = ki; self.kd = kd
        self.dt = dt
        self.integrator = 0.0
        self.prev_error = 0.0
        self.integrator_limit = integrator_limit

    def reset(self):
        self.integrator = 0.0
        self.prev_error = 0.0

    def step(self, setpoint, measurement):
        error = setpoint - measurement
        self.integrator += error * self.dt
        if self.integrator_limit:
            self.integrator = max(min(self.integrator, self.integrator_limit), -self.integrator_limit)
        derivative = (error - self.prev_error) / self.dt
        output = self.kp*error + self.ki*self.integrator + self.kd*derivative
        self.prev_error = error
        return output, error
