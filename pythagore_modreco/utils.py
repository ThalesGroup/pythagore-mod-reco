# Authors: Hélion du Mas des Bourboux <helion.dumasdesbourboux'at'thalesgroup.com>
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

import time
from tensorflow.keras.callbacks import Callback
from numpy.random import choice

class TimeHistory(Callback):
    """ Keras callback tto monitor execution time during training
    
    """
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, epoch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)



def split_dataset( data, labels,
                    p_train=0.8, p_valid=0.0, p_test=0.0,
                    ):
    """ Function to split and shuffle a dataset into train, validation and test
        splits.

        Arguments:
        data (tensor): input dataset
        labels (tensor): label vector associated to data 
        p_train (float): proportion of training data 
        p_valid (float): proportion of validation data
        p_test (float): proportion of test data 
    """
    
    def aux(D_ , L_,  p_, idx_):

        n_tot_examples_ = D_.shape[0]
        n_taken_examples_ = int(n_tot_examples_ * p_ )
        chosen_idx_ = choice(idx_ , size=n_taken_examples_, replace=False)
        free_indexes_ = list( set(idx_) - set( chosen_idx_ ) )

        return D_[chosen_idx_] , L_[chosen_idx_] , chosen_idx_, free_indexes_

    D = data
    L = labels

    idx = range(0, D.shape[0])
    X_train , Y_train, train_idx, free_idx = aux(D , L, p_train ,  idx)

    idx = free_idx
    X_valid , Y_valid, valid_idx, free_idx = aux(D , L, p_valid ,  idx)

    idx = free_idx
    X_test, Y_test, test_idx,free_idx = aux(D , L, p_test ,  idx)

    return X_train , Y_train , train_idx, X_valid , Y_valid, valid_idx, X_test , Y_test,test_idx