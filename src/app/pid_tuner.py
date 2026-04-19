class PIDController:
    def __init__(self):
        self.Kp = 1.0
        self.Ki = 0.0
        self.Kd = 0.0

    def tune(self, error_stats):
        # No-op tuner for local development
        return None
class PIDController:
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.error_sum = 0.0
        self.last_error = 0.0

    def update(self, error: float, dt: float) -> float:
        self.error_sum += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.Kp * error + self.Ki * self.error_sum + self.Kd * derivative
        self.last_error = error
        return output

    def tune(self, error_stats: dict):
        noise = error_stats.get("noise_variance", 0.0)
        bias = error_stats.get("bias_trend", 0.0)
        anticipation = error_stats.get("anticipation", 0.0)

        if noise > 1.0:
            self.Kp *= 0.9
            self.Kd *= 0.8
        if abs(bias) > 0.5:
            self.Ki += 0.01 * bias
        if abs(anticipation) > 0.5:
            self.Kd += 0.05 * anticipation

        self.Kp = max(0.1, min(self.Kp, 10.0))
        self.Ki = max(0.0, min(self.Ki, 5.0))
        self.Kd = max(0.0, min(self.Kd, 5.0))
