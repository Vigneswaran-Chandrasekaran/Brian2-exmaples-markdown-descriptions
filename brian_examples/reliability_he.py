from brian2 import *
from brian2tools import mdexport
from brian2tools.mdexport import MdExpander
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--github_md', type=bool, default=False, help='Github md')
parser.add_argument('--filename', type=str, default='', help='File name')
parser.add_argument('--brian_verbose', type=bool, default=False,
                    help='Brian verbose')

args = parser.parse_args()

custom = MdExpander(brian_verbose=args.brian_verbose, github_md=args.github_md)
set_device('markdown', expander=custom, filename=args.filename)

'''
Reliability of spike timing.

See e.g. Mainen & Sejnowski (1995) for experimental results in vitro.
'''

# The common noisy input
N = 25
tau_input = 5*ms
input = NeuronGroup(1, 'dx/dt = -x / tau_input + (2 /tau_input)**.5 * xi : 1')

# The noisy neurons receiving the same input
tau = 10*ms
sigma = .015
eqs_neurons = '''
dx/dt = (0.9 + .5 * I - x) / tau + sigma * (2 / tau)**.5 * xi : 1
I : 1 (linked)
'''
neurons = NeuronGroup(N, model=eqs_neurons, threshold='x > 1',
                      reset='x = 0', refractory=5*ms, method='euler')
neurons.x = 'rand()'
neurons.I = linked_var(input, 'x') # input.x is continuously fed into neurons.I
spikes = SpikeMonitor(neurons)

run(500*ms)
