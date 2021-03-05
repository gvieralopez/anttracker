import numpy as np



class LE:
	"""
	Random Walk class from a multidimensional Langevin Equation.
	"""

	def __init__(self, T:float, tau:float, noise_params:dict, 
				dim:int=1, N:int=1, dt:int=1):

		# siulation parameters
		self.T = T                    # total time
		self.dt = dt                  # time step of the simulation
		self.N = N                    # number of trials
		self.n = int(T / dt)          # number of time steps
		self.size = (self.n, dim, N)  # shape of the dynamic variables

		# model parameters
		self.tau = tau                    # relaxation characteristic time
		self.noise_params = noise_params  # noise properties (keys: 'pdf_name', 'scale')
		self.noise = np.ndarray           # noise array that will be fill in get_noise method

		# dynamic variables
		self.t = np.linspace(0, T, num=self.n)  # time array
		self.r = np.empty(self.size)            # position array
		self.v = np.empty(self.size)            # velocity array

		# initial conditions
		self.r0 = np.zeros((dim, self.N))
		self.v0 = np.zeros((dim, self.N))
		self._r0_ = False                  # True if initial positions are set by the user
		self._v0_ = False                  # True if initial velocities are set by the user



