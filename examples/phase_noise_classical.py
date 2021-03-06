import numpy
import time
import math

from beclab import *

def testPhaseNoise(gpu):
	constants = Constants(Model(N=40000, detuning=-41, nvx=16, nvy=16, nvz=128,
		ensembles=4, e_cut=1e6), double=(False if gpu else True))
	env = envs.cuda() if gpu else envs.cpu()
	evolution = SplitStepEvolution(env, constants)
	pulse = Pulse(env, constants)
	a = VisibilityCollector(env, constants, verbose=True)
	n = PhaseNoiseCollector(env, constants, verbose=True)

	gs = GPEGroundState(env, constants)

	cloud = gs.createCloud()
	cloud.createEnsembles()

	pulse.apply(cloud, 0.5 * math.pi, matrix=True, theta_noise=0.5 * math.pi / math.sqrt(constants.N))

	t1 = time.time()
	evolution.run(cloud, 0.05, callbacks=[n, a], callback_dt=0.0025, noise=False)
	env.synchronize()
	t2 = time.time()
	print "Time spent: " + str(t2 - t1) + " s"

	times, vis = a.getData()
	vis = XYData("noise", times, vis, ymin=0, ymax=1,
		xname="Time, ms", yname="Visibility")
	vis = XYPlot([vis])
	vis.save('phase_noise_classical_visibility_' + str(env) + '.pdf')

	times, noise = n.getData()
	XYPlot([XYData("test", times * 1000, noise, ymin=0, xname="Time, ms")]).save(
		'phase_noise_classical_' + str(env) + '.pdf')

	env.release()

testPhaseNoise(True)
testPhaseNoise(False)