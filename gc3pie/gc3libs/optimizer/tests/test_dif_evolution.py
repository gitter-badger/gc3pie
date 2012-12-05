#! /usr/bin/env python
#
"""
"""
# Copyright (C) 2011, 2012, GC3, University of Zurich. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
__docformat__ = 'reStructuredText'
__version__ = '$Revision$'

import os
import logging

from nose.tools import raises
from nose.plugins.skip import SkipTest

import numpy as np

from gc3libs.optimizer.dif_evolution import DifferentialEvolutionSequential


def rosenbrock_fn(vectors):
    result = []
    for vector in vectors:
        #---Rosenbrock saddle-------------------------------------------
        F_cost = 100 * ( vector[1] - vector[0]**2 )**2 + ( 1 - vector[0] )**2

        result.append(F_cost)
    return np.array(result)


def test_differential_evolution_with_rosenbrock():

    # FVr_minbound,FVr_maxbound   vector of lower and bounds of initial population
    #               the algorithm seems to work especially well if [FVr_minbound,FVr_maxbound]
    #               covers the region where the global minimum is expected
    #               *** note: these are no bound constraints!! ***
    dim = 2
    lower_bounds = -2 * np.ones(dim)
    upper_bounds = +2 * np.ones(dim)
        
    log = logging.getLogger("gc3.gc3libs")
	
    opt = DifferentialEvolutionSequential(
        dim = dim,          # number of parameters of the objective function
        lower_bds = lower_bounds,
        upper_bds = upper_bounds,
        target_fn=rosenbrock_fn,
        pop_size = 100,     # number of population members
        de_step_size = 0.85,# DE-stepsize ex [0, 2]
        prob_crossover = 1, # crossover probabililty constant ex [0, 1]
        itermax = 200,      # maximum number of iterations (generations)
        x_conv_crit = None, # stop when variation among x's is < this
        y_conv_crit = 1e-5, # stop when ofunc < y_conv_crit
        de_strategy = 'DE_local_to_best',
        logger = log,
        )

    # run the Diff.Evo. algorithm
    opt.de_opt()

    assert opt.has_converged()
    assert (opt.bestval - 0.) < opt.y_conv_crit
    assert (opt.best[0] - 1.) < 1e-3
    assert (opt.best[1] - 1.) < 1e-3