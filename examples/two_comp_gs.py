import numpy
import time
import math

from beclab import *

def testTwoCompGS(gpu):

	# preparation
	env = envs.cuda() if gpu else envs.cpu()
	constants = Constants(Model(N=150000), double=False if gpu else True)
	gs = GPEGroundState(env, constants)
	sp = SliceCollector(env, constants, pulse=None)

	# in fact, accurate two-component ground state calculations requires
	# precision of at least 1e-8, but this is just a test
	cloud = gs.createCloud(two_component=True, precision=1e-7)
	sp(0, cloud)

	# render
	times, a_xy, a_yz, b_xy, b_yz = sp.getData()

	a_data = HeightmapData("1st component", a_yz[0].transpose(),
		xmin=-constants.zmax * 1e6, xmax=constants.zmax * 1e6,
		xname="Z, $\\mu$m", yname="Y, $\\mu$m",
		ymin=-constants.ymax * 1e6, ymax=constants.ymax * 1e6, zmin=0)
	a_plot = HeightmapPlot(a_data)

	b_data = HeightmapData("2nd component", b_yz[0].transpose(),
		xmin=-constants.zmax * 1e6, xmax=constants.zmax * 1e6,
		xname="Z, $\\mu$m", yname="Y, $\\mu$m",
		ymin=-constants.ymax * 1e6, ymax=constants.ymax * 1e6, zmin=0)
	b_plot = HeightmapPlot(b_data)

	env.release()

	return a_plot, b_plot

print "CPU variant"
p1, p2 = testTwoCompGS(False)
p1.save("two_comp_gs_cpu_a.pdf")
p2.save("two_comp_gs_cpu_b.pdf")

print "GPU variant"
p1, p2 = testTwoCompGS(True)
p1.save("two_comp_gs_gpu_a.pdf")
p2.save("two_comp_gs_gpu_b.pdf")