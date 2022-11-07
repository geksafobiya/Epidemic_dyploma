import numpy as np
np.seterr(all='raise')

class GrowthCalculator(object):
    def __init__(self):
        # SIR equation coefficients
      #  self.Susceptible = 20.0 #сприятливі до інфекції
      #  self.Recovered = 10.0 #очухавшиєся
        self.gamma = 1.0 #швидкість одужання
        self.beta = 1.0 #константа швидкості
      #  self.Infectious = 10.0
        # Other parameters
        self.dt = 0.02
        self.iterations = 1000

        self.sus = 5
        self.inf = 4
        self.rec = 10

    def dS(self, Susceptible, Infectious, Recovered):
        dS_dt = -(self.beta*Susceptible*Infectious)/(Susceptible+Infectious+Recovered)
        return dS_dt

    def dI(self, Susceptible, Infectious, Recovered):
        dI_dt = (self.beta*Susceptible*Infectious)/(Susceptible+Infectious+Recovered) - self.gamma*Infectious
        return dI_dt

    def dR(self, Susceptible, Infectious, Recovered):
        dR_dt = self.gamma*Infectious
        # Calculate the predator population change
        return dR_dt

    def calculate(self):
         # import json

        susceptible_history = []
        infectious_history = []
        recovered_history = []

        y0 = np.array([self.sus, self.inf, self.rec], dtype='double')
        tspan = np.array([0.0, self.dt * self.iterations], dtype='double')

        try:
            t, y = self.rk4(self.derivatives, tspan, y0, self.iterations)
            susceptible_history = y[:, 0]
            infectious_history = y[:, 1]
            recovered_history = y[:, 2]

            print('t = ', t)
            #print(predator_history)
            #res = [dict([(ti, yi)]) for ti, yi in zip(t, predator_history)]
            #print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError):
            print("")

        return {
            'Susceptible': susceptible_history,
            'Infectious': infectious_history,
            'Recovered': recovered_history
        }

    def calculate_r0(self, beta, gamma):
        R0 = beta / gamma
        return R0

    def calculate_trecovery(self, gamma):
        t_recovery = 1 / gamma
        return t_recovery

    def derivatives(self, t, rf):

        Susceptible = rf[0]
        Infectious = rf[1]
        Recovered = rf[2]

        dSdt = self.dS(Susceptible, Infectious, Recovered)
        dIdt = self.dI(Susceptible, Infectious, Recovered)
        dRdt = self.dR(Susceptible, Infectious, Recovered)

        drfdt = np.array([dSdt, dIdt, dRdt], dtype='double')
        return drfdt


    def rk4(self, dydt, tspan, y0, n):
        # RK4 approximates the solution to an ODE using the RK4 method.
        #  Input:
        #    function dydt: points to a function that evaluates the right
        #                   hand side of the ODE.
        #    real tspan[2]: contains the initial and final times.
        #    real y0[m]: an array containing the initial condition.
        #    integer n: the number of steps to take.

        #  Output:
        #    real t[n+1], y[n+1,m]: the times and solution values.
        #

        if np.ndim(y0) == 0:
            m = 1
        else:
            m = len(y0)

        tfirst = tspan[0]
        tlast = tspan[1]
        dt = (tlast - tfirst) / n
        t = np.zeros(n + 1)
        y = np.zeros([n + 1, m])
        y[0, :] = y0

        for i in range(0, n):
            f1 = dydt(t[i], y[i, :])
            f2 = dydt(t[i] + dt / 2.0, y[i, :] + dt * f1 / 2.0)
            f3 = dydt(t[i] + dt / 2.0, y[i, :] + dt * f2 / 2.0)
            f4 = dydt(t[i] + dt, y[i, :] + dt * f3)

            t[i + 1] = t[i] + dt
            y[i + 1, :] = y[i, :] + dt * (f1 + 2.0 * f2 + 2.0 * f3 + f4) / 6.0

        return t, y
