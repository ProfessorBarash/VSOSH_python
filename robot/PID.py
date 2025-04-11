import time


def millis():
    return round(time.time() * 1000)


class PID_regulator:
    def __init__(self, P_coeff: float, I_coeff: float, D_coeff: float) -> None:
        """
        set up PID-regulator
        input:
            P_coeff - proportional gain
            I_coeff - integral coefficient
            D_coeff - differential coefficient
        """
        self.P_coeff = P_coeff
        self.I_coeff = I_coeff
        self.D_coeff = D_coeff
        self.last_U = 0 # последнее воздействие
        self.errors = [0, 0, 0]
        self.last_time = millis()

    def compute_PID(self, err: float) -> float:
        """
        main function wich compute controll value
        input:
            err - Current error
        output:
            U - controll value
        """
        dt = millis() - self.last_time
        self.last_time = millis()
        integral_discr_coeff = self.I_coeff * dt
        differential_discr_coeff = self.D_coeff / dt

        # обновление списка ошибок
        self.errors[0] = self.errors[1]
        self.errors[1] = self.errors[2]
        self.errors[2] = err

        P = self.P_coeff * (self.errors[-1] - self.errors[-2])
        I = integral_discr_coeff * self.errors[-1]
        D = differential_discr_coeff * (self.errors[-1] - 2 * self.errors[-2] + self.errors[-3])

        U = self.last_U + P + I + D
        self.last_U = U

        return U

    def clear_PID(self) -> None:
        """
        reboot PID for new target
        """
        self.last_U = 0
        self.errors = [0, 0, 0]