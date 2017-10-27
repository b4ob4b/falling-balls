import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.patches import Circle
from matplotlib import animation


class Box:

    def __init__(self,
                 gravity=-9.81,
                 boarder_left=0,
                 boarder_bottom=0,
                 boarder_right=10,
                 boarder_top=10
                 ):
        self.gravity = gravity
        self.boarder_top = boarder_top
        self.boarder_right = boarder_right
        self.boarder_bottom = boarder_bottom
        self.boarder_left = boarder_left

    def plot_box(self):

        fig = plt.figure()
        ax = plt.subplot(
            xlim = (self.boarder_left -1, self.boarder_right + 1),
            ylim = (self.boarder_bottom - 1, self.boarder_top + 1)
        )
        ax.plot([self.boarder_left, self.boarder_left], [self.boarder_bottom + 0.001, self.boarder_top],'k')
        ax.plot([self.boarder_right, self.boarder_right], [self.boarder_bottom + 0.001, self.boarder_top],'k')
        ax.plot([self.boarder_left, self.boarder_right], [self.boarder_bottom, self.boarder_bottom],'k')
        ax.plot([self.boarder_left, self.boarder_right], [self.boarder_top, self.boarder_top],'k')
        return fig, ax

class Ball(Box):

    # mass = 1 # kg
    # radius = 1 # m
    # gravity = -9.81  # m / s**2

    def __init__(self,
                 X0 = 2., # m
                 Y0 = 2., # m
                 VX0 = 0, # m/s
                 VY0 = 1, # m/s
                 radius = 1,
                 temperature = 20, # Celcius
                 mass = 1, # kg
                 gravity= -9.81,  # m
                 boarder_left=0,
                 boarder_bottom=0,
                 boarder_right=10,
                 boarder_top=10
                 ):
        self.position_y = Y0
        self.position_x = X0
        self.velocity_y = VY0
        self.velocity_x = VX0
        self.radius = radius
        self.mass = mass
        self.temperature = temperature
        Box.__init__(self,gravity,boarder_left,boarder_bottom,boarder_right,boarder_top)

        self.state_y = self.position_y, self.velocity_y
        self.state_x = self.position_x, self.velocity_x
        self.time_elapsed = 0

        if self.position_x - self.radius < self.boarder_left:
            raise ValueError('The ball seems to be placed too far left: %s - %s > %s' % (self.position_x,self.radius, self.boarder_left))

    def dt_state(self,state,dt,a):
        "steps a particle's position and velocity subject to acceleration a"
        y, dy = state
        ddy = a
        return dy, ddy

    def hit_wall(self):
        if self.position_x - self.radius < self.boarder_left:
            self.velocity_x = -self.velocity_x
            self.state_x = self.position_x, self.velocity_x
        if self.position_x + self.radius > self.boarder_right:
            self.velocity_x = -self.velocity_x
            self.state_x = self.position_x, self.velocity_x
        if self.position_y - self.radius < self.boarder_bottom:
            self.velocity_y = -self.velocity_y
            self.state_y = self.position_y, self.velocity_y
        if self.position_y + self.radius > self.boarder_top:
            self.velocity_y = -self.velocity_y
            self.state_y = self.position_y, self.velocity_y

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
        # if self.position_y < self.radius:
        #     self.velocity_y = abs(self.velocity_y)
        #     self.state_y = self.position_y, self.velocity_y
        self.time_elapsed += dt
        self.hit_wall()


ball = Ball(5,5,5,10)
dt = 1/30
time_elapsed = [0]
fig, ax = ball.plot_box()
ax.grid()

patch = Circle((5, -5), ball.radius, fc='y')

def init():
    patch.center = (2, 0)
    ax.add_patch(patch)
    return patch,

def animate(i):
    global ball, dt, time_elapsed
    ball.step(dt)
    time_elapsed.append(ball.time_elapsed)

    x = ball.position_x
    y = ball.position_y
    patch.center = (x, y)
    return patch,


ani = animation.FuncAnimation(fig, animate, frames=10,interval=100, blit=True, init_func=init)
