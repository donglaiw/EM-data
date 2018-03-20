#!/usr/bin/env python
__doc__ = """

Out-of-focus (Gaussian blur) section augmentation.

Kisuk Lee <kisuklee@mit.edu>, 2017
"""

import numpy as np
from scipy.ndimage.filters import gaussian_filter

from em_data.augmentor import DataAugment

class Blur(DataAugment):
    """
    Introduce out-of-focus section(s) to a training example.

    The number of out-of-focus sections to introduce is randomly drawn from the
    uniform distribution between [0, MAX_SEC]. Default MAX_SEC is 1, which can
    be overwritten by user-specified value. Out-of-focus process is implemented
    with Gaussian blurring.
    """

    def __init__(self, max_sec=1, sigma_max=5.0, mode='full', skip_ratio=0.3):
        """Initialize parameters.

        Args:
            max_sec: Maximum number of out-of-foucs sections.
            sigma_max: Maximum width for Gaussian blur filter.
            mode: 'full', 'partial', 'mix'
            skip_ratio: Probability of skipping augmentation.
        """
        self.set_max_sections(max_sec)
        self.set_sigma_max(sigma_max)
        self.set_mode(mode)
        self.set_skip_ratio(skip_ratio)

    def prepare(self, spec, **kwargs):
        # No change in spec.
        self.skip = np.random.rand() < self.skip_ratio
        return spec

    def __call__(self, sample, **kwargs):
        if not self.skip:
            sample = self.augment(sample, **kwargs)
        return sample

    def augment(self, sample, **kwargs):
        """Apply out-of-section section data augmentation."""
        # Randomly draw the number of sections to introduce.
        num_sec = np.random.randint(1, self.MAX_SEC + 1)

        # DEBUG(kisuk)
        # print "\n[Blur]"
        # print "num_sec = %d" % num_sec

        # Assume that the sample contains only one input volume, or multiple
        # input volumes of same size.
        imgs = kwargs['imgs']
        dims = set([])
        for key in imgs:
            dim = sample[key].shape[-3:]
            assert num_sec < dim[-3]
            dims.add(dim)
        assert len(dims) == 1
        dim  = dims.pop()
        xdim = dim[-1]
        ydim = dim[-2]
        zdim = dim[-3]

        # Randomly draw z-slices to blur.
        zlocs = sorted(np.random.choice(zdim, num_sec, replace=False))

        # Apply full or partial missing sections according to the mode.
        if self.mode == 'full':
            for z in zlocs:
                for key in imgs:
                    sigma = np.random.rand() * self.sigma_max
                    img = sample[key][...,z,:,:]
                    sample[key][...,z,:,:] = gaussian_filter(img, sigma=sigma)
                    # DEBUG(kisuk)
                    # print 'z = {}, sigma = {}'.format(z+1,sigma)
        else:
            for z in zlocs:
                # Random sigma.
                sigma = np.random.rand() * self.sigma_max
                # DEBUG(kisuk)
                # print 'z = {}, sigma = {}'.format(z+1,sigma)
                # Blurring.
                for key in imgs:
                    img = sample[key][...,z,:,:]
                    img = gaussian_filter(img, sigma=sigma)
                    # Full or partial?
                    if self.mode == 'mix' and np.random.rand() > 0.5:
                        # Full image blurring.
                        sample[key][...,z,:,:] = img
                    else:
                        # Draw a random xy-coordinate.
                        x = np.random.randint(0, xdim)
                        y = np.random.randint(0, ydim)
                        rule = np.random.rand(4) > 0.5
                        # 1st quadrant.
                        if rule[0]:
                            sample[key][...,z,:y,:x] = img[...,:y,:x]
                        # 2nd quadrant.
                        if rule[1]:
                            sample[key][...,z,y:,:x] = img[...,y:,:x]
                        # 3nd quadrant.
                        if rule[2]:
                            sample[key][...,z,:y,x:] = img[...,:y,x:]
                        # 4nd quadrant.
                        if rule[3]:
                            sample[key][...,z,y:,x:] = img[...,y:,x:]

        return sample

    ####################################################################
    ## Setters.
    ####################################################################

    def set_max_sections(self, max_sec):
        """Set the maximum number of missing sections to introduce."""
        assert max_sec >= 0
        self.MAX_SEC = max_sec

    def set_skip_ratio(self, ratio):
        """Set the probability of skipping augmentation."""
        assert ratio >= 0.0 and ratio <= 1.0
        self.skip_ratio = ratio

    def set_mode(self, mode):
        """Set full/partial/mix missing section mode."""
        assert mode=='full' or mode=='partial' or mode=='mix'
        self.mode = mode

    def set_sigma_max(self, sigma_max):
        """Set the maximum sigma of the Gaussian blur filter."""
        assert sigma_max >= 0
        self.sigma_max = sigma_max
