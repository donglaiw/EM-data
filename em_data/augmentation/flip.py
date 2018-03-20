#!/usr/bin/env python
__doc__ = """
Random flip augmentation.
Kisuk Lee <kisuklee@mit.edu>, 2017
"""
import numpy as np

from em_segLib.transform import flip
from em_data.augmentor import DataAugment

class Flip(DataAugment):
    """
    Random flip.
    """

    def __init__(self, **kwargs):
        pass

    def prepare(self, spec, **kwargs):
        # No change in sample spec.
        return spec

    def __call__(self, sample, **kwargs):
        # Determine how to flip.
        if 'rule' in kwargs:
            rule = kwargs['rule']
        else:
            rule = np.random.rand(4) > 0.5
        # Apply flip.
        for k, v in sample.iteritems():
            sample[k] = flip(v, rule)
        return sample
