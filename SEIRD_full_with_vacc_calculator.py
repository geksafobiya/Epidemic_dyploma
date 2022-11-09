import numpy as np
np.seterr(all='raise')

class SEIRDvaccCalculator(object):
    def __init__(self):
        # SIR equation coefficients
      #  self.Susceptible = 20.0 #сприятливі до інфекції
      #  self.Recovered = 10.0 #очухавшиєся
        self.gamma_unvac = 1.0 #швидкість одужання
        self.gamma_vacc = 1.0

        self.beta_unvac_unvac = 1.0 #константа швидкості
        self.beta_unvac_vac = 1.0
        self.beta_vac_unvac = 1.0
        self.beta_vac_vac = 1.0

        self.alpha_unvac = 1.0
        self.alpha_vac = 1.0

        self.theta_unvac = 1.0
        self.theta_vac = 1.0

        self.mu = 1.0
        self.l = 1.0

      #  self.Infectious = 10.0
        # Other parameters
        #self.dt = 0.02

        self.days = 100

        self.exp_vac = 5
        self.exp_unvac = 5
        self.sus_unvac = 5
        self.sus_vac = 5
        self.inf_unvac = 4
        self.inf_vac = 4
        self.rec_unvac = 0
        self.rec_vac = 0
        self.dead = 0

    def dS_unvac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dS_unvac_dt = self.l - self.mu*Susceptible_unvac \
                      - (self.beta_unvac_unvac*Infectious_unvac + self.beta_unvac_vac*Infectious_vac)*Susceptible_unvac\
                      /(Susceptible_unvac+Susceptible_vac+Exposed_unvac+Exposed_vac+Infectious_unvac+Infectious_vac+Recovered_unvac+Recovered_vac)
        return dS_unvac_dt

    def dS_vac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dS_vac_dt = - self.mu*Susceptible_vac \
                    - (self.beta_vac_unvac*Infectious_unvac + self.beta_vac_vac*Infectious_vac)*Susceptible_vac\
                    /(Susceptible_unvac+Susceptible_vac+Exposed_unvac+Exposed_vac+Infectious_unvac+Infectious_vac+Recovered_unvac+Recovered_vac)
        return dS_vac_dt

    def dE_unvac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dE_unvac_dt = (self.beta_unvac_unvac*Infectious_unvac + self.beta_unvac_vac*Infectious_vac)*Susceptible_unvac\
                      /(Susceptible_unvac+Susceptible_vac+Exposed_unvac+Exposed_vac+Infectious_unvac+Infectious_vac+Recovered_unvac+Recovered_vac) \
                      - (self.mu + self.alpha_unvac)*Exposed_unvac
        return dE_unvac_dt

    def dE_vac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dE_vac_dt = (self.beta_unvac_vac*Infectious_unvac + self.beta_vac_vac*Infectious_vac)*Susceptible_vac\
                    /(Susceptible_unvac+Susceptible_vac+Exposed_unvac+Exposed_vac+Infectious_unvac+Infectious_vac+Recovered_unvac+Recovered_vac) \
                    - (self.mu + self.alpha_vac)*Exposed_vac
        return dE_vac_dt

    def dI_unvac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dI_unvac_dt = self.alpha_unvac*Exposed_unvac \
                      - (self.gamma_unvac+self.mu+self.theta_unvac)*Infectious_unvac
        return dI_unvac_dt

    def dI_vac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dI_vac_dt = self.alpha_vac*Exposed_vac \
                    - (self.gamma_vac+self.mu+self.theta_vac)*Infectious_vac
        return dI_vac_dt

    def dR_unvac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dR_unvac_dt = self.gamma_unvac*Infectious_unvac \
                      - self.mu*Recovered_unvac
        # Calculate the predator population change
        return dR_unvac_dt

    def dR_vac(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dR_vac_dt = self.gamma_vac*Infectious_vac \
                    - self.mu*Recovered_vac
        # Calculate the predator population change
        return dR_vac_dt

    def dD(self, Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac, Infectious_vac, Recovered_unvac, Recovered_vac, Dead):
        dD_dt = self.theta_unvac*Infectious_unvac \
                + self.theta_vac*Infectious_vac \
                + self.mu*(Susceptible_unvac+Susceptible_vac+Exposed_unvac+Exposed_vac+Infectious_unvac+Infectious_vac+Recovered_unvac+Recovered_vac)
        # Calculate the predator population change
        return dD_dt


    def calculate(self):
         # import json

        susceptible_unvac_history = []
        susceptible_vac_history = []
        exposed_unvac_history = []
        exposed_vac_history = []
        infectious_unvac_history = []
        infectious_vac_history = []
        recovered_unvac_history = []
        recovered_vac_history = []
        dead_history = []

        y0 = np.array([self.sus_unvac, self.sus_vac, self.exp_unvac, self.exp_vac,
                       self.inf_unvac, self.inf_vac, self.rec_unvac, self.rec_vac,
                       self.dead], dtype='double')
        tspan = np.array([0.0, self.days], dtype='double')

        try:
            t, y = self.rk4(self.derivatives, tspan, y0, self.days)

            susceptible_unvac_history = y[:, 0]
            susceptible_vac_history = y[:, 1]
            exposed_unvac_history = y[:, 2]
            exposed_vac_history = y[:, 3]
            infectious_unvac_history = y[:, 4]
            infectious_vac_history = y[:, 5]
            recovered_unvac_history = y[:, 6]
            recovered_vac_history = y[:, 7]
            dead_history = y[:, 8]


            print('t = ', t)
            #print(predator_history)
            #res = [dict([(ti, yi)]) for ti, yi in zip(t, predator_history)]
            #print(json.dumps(res, indent=2))
        except (RuntimeError, OverflowError, FloatingPointError):
            print("")

        return {
            'Susceptible_unvac': susceptible_unvac_history,
            'Susceptible_vac': susceptible_vac_history,
            'Exposed_unvac': exposed_unvac_history,
            'Exposed_vac': exposed_vac_history,
            'Infectious_unvac': infectious_unvac_history,
            'Infectious_vac': infectious_vac_history,
            'Recovered_unvac': recovered_unvac_history,
            'Recovered_vac': recovered_vac_history,
            'Dead': dead_history
        }

    def derivatives(self, t, rf):
        Susceptible_unvac = rf[0]
        Susceptible_vac = rf[1]
        Exposed_unvac = rf[2]
        Exposed_vac = rf[3]
        Infectious_unvac = rf[4]
        Infectious_vac = rf[5]
        Recovered_unvac = rf[6]
        Recovered_vac = rf[7]
        Dead = rf[8]

        dS_unvac_dt = self.dS_unvac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                    Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dS_vac_dt = self.dS_vac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dE_unvac_dt = self.dE_unvac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                    Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dE_vac_dt = self.dE_vac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dI_unvac_dt = self.dI_unvac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                    Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dI_vac_dt = self.dI_vac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dR_unvac_dt = self.dR_unvac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                    Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dR_vac_dt = self.dR_vac(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                                Infectious_vac, Recovered_unvac, Recovered_vac, Dead)
        dD_dt = self.dD(Susceptible_unvac, Susceptible_vac, Exposed_unvac, Exposed_vac, Infectious_unvac,
                        Infectious_vac, Recovered_unvac, Recovered_vac, Dead)

        drfdt = np.array([dS_unvac_dt, dS_vac_dt, dE_unvac_dt, dE_vac_dt, dI_unvac_dt,
                          dI_vac_dt, dR_unvac_dt, dR_vac_dt, dD_dt], dtype='double')
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
