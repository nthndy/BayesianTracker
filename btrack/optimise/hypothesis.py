#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:     BayesianTracker
# Purpose:  A multi object tracking library, specifically used to reconstruct
#           tracks in crowded fields. Here we use a probabilistic network of
#           information to perform the trajectory linking. This method uses
#           positional and visual information for track linking.
#
# Authors:  Alan R. Lowe (arl) a.lowe@ucl.ac.uk
#
# License:  See LICENSE.md
#
# Created:  14/08/2014
#-------------------------------------------------------------------------------

__author__ = "Alan R. Lowe"
__email__ = "a.lowe@ucl.ac.uk"

import os
import numpy as np
import ctypes
import json

H_TYPES = ['P_FP','P_init','P_term','P_link','P_branch','P_dead','P_merge']


class Hypothesis(ctypes.Structure):
    """ Hypothesis structure

      This is essentially a replicate of the C-structure used by the hypothesis
      engine. Added a few extra functions to enable quick assignment.

      unsigned int hypothesis;
      unsigned int ID;
      double probability;
      unsigned int link_ID;
      unsigned int child_one_ID;
      unsigned int child_two_ID;

      Notes:
        These are automatically generated by the optimiser
    """
    _fields_ = [('hypothesis',ctypes.c_uint),
                ('ID',ctypes.c_uint),
                ('probability',ctypes.c_double),
                ('link_ID', ctypes.c_uint),
                ('child_one_ID', ctypes.c_uint),
                ('child_two_ID', ctypes.c_uint),
                ('parent_one_ID', ctypes.c_uint),
                ('parent_two_ID', ctypes.c_uint)]

    @property
    def type(self):
        return H_TYPES[self.hypothesis]

    @property
    def score(self):
        raise DeprecationWarning('score is deprecated. Use log_likelihood now.')

    @property
    def log_likelihood(self):
        return self.probability




class PyHypothesisParams(ctypes.Structure):
    """ HypothesisParams

    A convenient way to send hypothesis generation parameters to the hypothesis
    engine.

      double lambda_time;   // lambda_1
      double lambda_dist;   // lambda_2
      double lambda_link;   // lambda_3
      double lambda_branch; // lambda_4
      double eta;           // default low probability
      double theta_dist;
      double theta_time;
      double dist_thresh;
      double time_thresh;
      unsigned int apop_thresh;
      double segmentation_miss_rate;
      double apoptosis_rate;
      bool relax;

    Notes:
        None

    """
    _fields_ = [('lambda_time', ctypes.c_double),
                ('lambda_dist', ctypes.c_double),
                ('lambda_link', ctypes.c_double),
                ('lambda_branch', ctypes.c_double),
                ('eta', ctypes.c_double),
                ('theta_dist', ctypes.c_double),
                ('theta_time', ctypes.c_double),
                ('dist_thresh', ctypes.c_double),
                ('time_thresh', ctypes.c_double),
                ('apop_thresh', ctypes.c_uint),
                ('segmentation_miss_rate', ctypes.c_double),
                ('apoptosis_rate', ctypes.c_double),
                ('relax', ctypes.c_bool),
                ('hypotheses_to_generate', ctypes.c_uint)]

    def __init__(self, name=None):
        self.name = name

    @staticmethod
    def load(filename):
        return read_hypothesis_model(filename)






# def read_hypothesis_model(filename):
def read_hypothesis_model(config):
    """ read_hypothesis_model

    Read in a set of hypothesis parameters from a JSON description file.  The
    JSON file should contain the parameters of the PyHypothesisParams structure,
    and the function will return an instantiated PyHypothesisParams to be
    passed to the optimisation engine.

    Args:
        filename: the filename of the parameter file

    Notes:
        None
    """

    h_params = PyHypothesisParams()
    fields = [f[0] for f in h_params._fields_]

    # with open(filename, 'r') as json_file:
    #     config = json.load(json_file)

    for p in config['HypothesisModel']:
        if p in fields:
            setattr(h_params, p, config['HypothesisModel'][p])

    h_params.name = config['HypothesisModel']['name']

    # finally, take the hypotheses and setup a mask to generate only the
    # specified hypotheses
    # TODO(arl): no need to specify FP, this should be always be generated
    hypotheses = config['HypothesisModel']['hypotheses']
    h_bin = ''.join([str(int(h)) for h in [h in hypotheses for h in H_TYPES]])
    h_params.hypotheses_to_generate = int(h_bin[::-1], 2)

    return h_params







if __name__ == '__main__':
    p = read_hypothesis_model('../models/MDCK_hypothesis.json')
    print p, p.eta
