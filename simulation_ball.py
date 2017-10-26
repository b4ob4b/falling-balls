import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.patches import Circle
from matplotlib import animation



# d2x / dt2 = 0
# dx / dt = vx
# dvx / dt = 0
#
# d2y / dt2 = gravity
# dy / dt = vy
# dvx / dt = gravity

class Ball:

    mass = 1 # kg
    radius = 1 # m
    gravity = -9.81  # m / s**2

    def __init__(self,
                 Y0 = 2., # m
                 X0 = 2., # m
                 VY0 = 1, # m/s
                 VX0 = 0  # m/s
                 ):
        self.position_y = Y0
        self.position_x = X0
        self.velocity_y = VY0
        self.velocity_x = VX0

        self.state_y = self.position_y, self.velocity_y
        self.state_x = self.position_x, self.velocity_x
        self.time_elapsed = 0

    def dt_state(self,state,dt,a):
        "steps a particle's position and velocity subject to acceleration a"
        y, dy = state
        ddy = a
        return dy, ddy

    def energy(self):
        kinetic = 0.5 * self.mass * self.velocity_y ** 2
        potential = self.mass * abs(self.gravity) * self.position_y
        return kinetic, potential

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.state_y = odeint(self.dt_state, self.state_y, [0,dt] , args=(self.gravity,))[1]
        self.state_x = odeint(self.dt_state, self.state_x, [0, dt], args=(0,))[1]
        self.position_y, self.velocity_y = self.state_y
        self.position_x, self.velocity_x = self.state_x
        if self.position_y < self.radius:
            self.velocity_y = abs(self.velocity_y)
            self.state_y = self.position_y, self.velocity_y
        self.time_elapsed += dt


ball = Ball(2,2,10,1)
dt = 1/30
time_elapsed = [0]
kin_energy = [ball.energy()[0] / 10]
pot_energy = [ball.energy()[1] / 10]
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, 20), ylim=(-2, 8))
ax.grid()
kin_energy_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
pot_energy_text = ax.text(0.02, 0.80, '', transform=ax.transAxes)

line_kin, = ax.plot([], [], 'r-', lw=2)
line_pot, = ax.plot([], [], 'b-', lw=2)
patch = Circle((5, -5), ball.radius, fc='y')

def init():
    patch.center = (2, 0)
    line_kin.set_data([], [])
    line_pot.set_data([], [])
    ax.add_patch(patch)
    kin_energy_text.set_text('')
    pot_energy_text.set_text('')
    return patch, kin_energy_text, pot_energy_text,line_kin, line_pot

def animate(i):
    global ball, dt, time_elapsed
    ball.step(dt)
    time_elapsed.append(ball.time_elapsed)
    kin_energy.append(ball.energy()[0] / 10)
    pot_energy.append(ball.energy()[1] / 10)
    line_kin.set_data(time_elapsed, kin_energy)
    line_pot.set_data(time_elapsed, pot_energy)
    x = ball.position_x
    y = ball.position_y
    patch.center = (x, y)
    kin_energy_text.set_text('kinetic energy = %.1f J' % ball.energy()[0])
    pot_energy_text.set_text('potential energy = %.1f J' % ball.energy()[1])
    return patch, kin_energy_text, pot_energy_text, line_kin, line_pot

 # 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=10,interval=100, blit=True, init_func=init)

# ani.save('animation_falling_ball.gif', writer='imagemagick', fps=10, dpi=80)
