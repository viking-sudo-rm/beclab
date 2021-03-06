import numpy
import time
import math

from beclab import *

def testVisibility(gpu, matrix_pulses):
	constants = Constants(Model(N=44000, nvx=8, nvy=8, nvz=64, e_cut=1e6),
		double=False if gpu else True)
	env = envs.cuda() if gpu else envs.cpu()
	evolution = SplitStepEvolution(env, constants)

	gs = GPEGroundState(env, constants)
	pulse = Pulse(env, constants)
	v = VisibilityCollector(env, constants)
	p = ParticleNumberCollector(env, constants, pulse=pulse, matrix_pulse=matrix_pulses)

	cloud = gs.createCloud()
	pulse.apply(cloud, math.pi * 0.5, matrix=matrix_pulses)

	t1 = time.time()
	evolution.run(cloud, 0.4, callbacks=[v, p], callback_dt=0.002)
	env.synchronize()
	t2 = time.time()
	print "Time spent: " + str(t2 - t1) + " s"

	name = str(env) + ", " + ("ideal" if matrix_pulses else "nonideal") + " pulses"

	times, vis = v.getData()
	vis = XYData(name, times, vis, ymin=0, ymax=1, xname="Time, s", yname="Visibility")

	times, N1, N2, N = p.getData()
	particles = XYData(name, times, (N1 - N2) / N,
		ymin=-1, ymax=1, xname="Time, s", yname="Population ratio")

	env.release()
	return particles, vis

visibility_data = []
particles_data = []
for gpu, matrix_pulses in ((False, True), (False, False), (True, True), (True, False)):
	p, v = testVisibility(gpu=gpu, matrix_pulses=matrix_pulses)
	visibility_data.append(v)
	particles_data.append(p)

XYPlot(visibility_data).save('visibility_noise_vis.pdf')
XYPlot(particles_data).save('visibility_noise_population.pdf')