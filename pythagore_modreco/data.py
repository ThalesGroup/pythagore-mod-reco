# Authors: Helion du Mas des Bourboux <helion.dumasdesbourboux'at'thalesgroup.com>
#         Thomas Courtat <thomas.courtat'at'thalesgroup.com>

# MIT License

# Copyright (c) 2021 Thales Six GTS France

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from h5py import File
from numpy import array, zeros, sqrt, mean, vstack
from numpy.random import choice
import pickle 

"""
Gathers function to open different datasets of interest
"""

def read_augmod(fname):
    """ Open Augmod dataset

    Args:
        fname (string): dataset path

    Returns:
        (dict): loaded dataset
    """
    data = dict()
    with File(fname,'r') as f:
        data['classes'] =[c.decode() for c in f['classes'] ]
        data['signals'] = array(f['signals'] )
        data['modulations'] = array(f['modulations'] )
        data['snr'] = array(f['snr'] )
        data['frequency_offsets'] = array(f['frequency_offsets'] )
    return data


def read_RML2016(fname='./2016.04C.multisnr.pkl',snrs=None,verbose=False):
    """ Open datasets from Radio Machine Learning 2016

    Args:
        fname (str, optional): [description]. Defaults to './2016.04C.multisnr.pkl'.
        snrs (list of int, optional): list of snrs to keep. If None keeps all.  Defaults to None.
        verbose (bool): set verbosity

    Returns:
        (tuple of arrays): data, labels, snrs, list of possible modulations
    """
    def _create_data_set(snrs_):

        X = []
        lbl = []
        snrX = []

        for mod in mods:
            for snr in snrs_:
                sigs = Xd[(mod,snr)]
                tmp_sigs = zeros((sigs.shape[0],sigs.shape[1]*sigs.shape[2]))
                tmp_sigs[:,:sigs.shape[2]] = sigs[:,0,:]
                tmp_sigs[:,sigs.shape[2]:] = sigs[:,1,:]
                norm = sqrt(mean(tmp_sigs**2,axis=1))
                X.append(Xd[(mod,snr)]/norm[:,None,None])
                for i in range(Xd[(mod,snr)].shape[0]):
                    lbl.append(mod)
                    snrX.append(snr)
        X = vstack(X)
        snrX = array(snrX)
        return array(X), array(lbl) , array(snrX)

    Xd = pickle.load(open(fname,'rb'), encoding='latin1')
    # Xd: dictionnary with 
    # keys = (str: modulation_name , int: snr) and 
    # values = tensor of signals which shape is (nb_of_signals, 2 , 128)

    mods_,snrs_ = list( zip( *Xd.keys() ) )
    snrs_ = sorted( list( set( snrs_ ) ) )
    mods = sorted( list( set( mods_ ) ) )

    if snrs is None:
        snrs = snrs_

    if verbose:
        print('List of signal SNR:')
        print(snrs)
        print('List of modulations under consideration:')
        print(mods)

    x,lab,s =  _create_data_set(snrs)
    lab =array( [ mods.index (l) for l in lab])

    return x,lab,s, mods


def read_RML2018(fName ,nb_examples = None):
    """ Open datasets from Radio Machine Learning 2018

    Args:
        fname (str, optional): [description]. Defaults to './2016.04C.multisnr.pkl'.
        snrs (list of int, optional): list of snrs to keep. If None keeps all.  Defaults to None.
        verbose (bool): set verbosity

    Returns:
        (tuple of arrays): data, labels, snrs, None
    """
    with File(fName,'r') as h:

        if not nb_examples is None:
            w = choice(h['X'].shape[0], size=nb_examples, replace=False)
            data = h['X'][:][w]
            mods_ = h['Y'][:][w]
            snrs_ = h['Z'][:][w]
        else:
            data = h['X'][:]
            mods_ = h['Y'][:]
            snrs_ = h['Z'][:]

    snrs_ = snrs_.flatten()
    snrs_=snrs_.reshape(-1)
    data = data.transpose((0,2,1))

    return data, mods_, snrs_,None