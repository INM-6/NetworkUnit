from networkunit.tests.test_two_sample_test import two_sample_test
from networkunit.capabilities.cap_ProducesSpikeTrains import ProducesSpikeTrains
from elephant.statistics import isi, lv, cv #, cv2
import numpy as np
from abc import ABCMeta, abstractmethod


class isi_variation_test(two_sample_test):
    """
    Test to compare the firing rates of a set of neurons in a network.
    """
    # __metaclass__ = ABCMeta

    required_capabilities = (ProducesSpikeTrains, )

    def generate_prediction(self, model, **kwargs):
        if kwargs:
            self.params.update(kwargs)
        if 'variation_measure' not in self.params:
            self.params.update(variation_measure = 'lv')
        if not hasattr(model, 'prediction'):
            model.prediction = {}
        if self.test_hash in model.prediction:
            isi_var = model.prediction[self.test_hash]
        else:
            spiketrains = model.produce_spiketrains(**self.params)
            isi_list = [isi(st) for st in spiketrains]
            if self.params['variation_measure'] == 'lv':
                isi_var = [lv(intervals) for intervals in isi_list]
            elif self.params['variation_measure'] == 'cv':
                isi_var = [cv(intervals) for intervals in isi_list]
            elif self.params['variation_measure'] == 'isi':
                isi_var = [float(item) for sublist in isi_list for item in sublist]
            else:
                raise ValueError, 'Variation measure not known.'
            model.prediction[self.test_hash] = isi_var
        return isi_var

