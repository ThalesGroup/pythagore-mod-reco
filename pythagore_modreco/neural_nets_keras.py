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

from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Input,
    AlphaDropout,
    GlobalAveragePooling1D,
    BatchNormalization,
    add,
)
from tensorflow.keras.layers import Flatten, Dense, Dropout, Reshape, Activation
from tensorflow.keras.layers import (
    Conv1D,
    AveragePooling1D,
    ZeroPadding2D,
    Convolution2D,
    MaxPooling1D,
    MaxPooling2D,
)


def get_LModCNN(input_shp, output_shp, verbose=False):
    """Generate LModCNN architecture as defined in Courtat and du Mas des Bourboux,
        A light neural network for modulation detection under impairments, ISNCC 2021

    Arguments:
        input_shp (list): shape of the input data [signal_length,2], batch is omitted
        output_shp (list): shape of the output data [n_classes]
        verbose (bool): set verbosity
    """
    model = Sequential()

    model.add(
        Conv1D(
            filters=8,
            kernel_size=7,
            activation="relu",
            padding="same",
            input_shape=input_shp,
        )
    )

    model.add(Conv1D(filters=16, kernel_size=7, activation="relu", padding="same"))

    model.add(Conv1D(filters=32, kernel_size=7, activation="relu", padding="same"))

    model.add(Conv1D(filters=64, kernel_size=7, activation="relu", padding="same"))

    model.add(GlobalAveragePooling1D())

    model.add(Dense(units=256, activation="relu", kernel_initializer="he_normal"))
    model.add(Dropout(rate=0.5))

    model.add(Dense(output_shp, activation="softmax", kernel_initializer="he_normal"))

    if verbose:
        model.summary()

    return model


def get_LModCNNResNetRelu(input_shp, output_shp, verbose=False):
    """Generate LMod CNN with residual connexion architecture as defined in Courtat and du Mas des Bourboux,
        A light neural network for modulation detection under impairments, ISNCC 2021

    Arguments:
        input_shp (list): shape of the input data [signal_length,2], batch is omitted
        output_shp (list): shape of the output data [n_classes]
        verbose (bool): set verbosity
    """
    kernel_size = 7

    X_input = Input(input_shp)

    X = Conv1D(
        filters=8,
        kernel_size=1,
        activation="relu",
        padding="same",
        input_shape=input_shp,
        kernel_initializer="glorot_uniform",
    )(X_input)

    X_shortcut = X

    X = Conv1D(
        filters=8,
        kernel_size=kernel_size,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = Conv1D(
        filters=8,
        kernel_size=kernel_size,
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = add([X, X_shortcut])
    X = Activation("relu")(X)

    X = Conv1D(
        filters=16,
        kernel_size=1,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)

    X_shortcut = X

    X = Conv1D(
        filters=16,
        kernel_size=kernel_size,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = Conv1D(
        filters=16,
        kernel_size=kernel_size,
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = add([X, X_shortcut])
    X = Activation("relu")(X)

    X = Conv1D(
        filters=32,
        kernel_size=1,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)

    X_shortcut = X

    X = Conv1D(
        filters=32,
        kernel_size=kernel_size,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = Conv1D(
        filters=32,
        kernel_size=kernel_size,
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = add([X, X_shortcut])
    X = Activation("relu")(X)

    X = Conv1D(
        filters=64,
        kernel_size=1,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)

    X_shortcut = X

    X = Conv1D(
        filters=64,
        kernel_size=kernel_size,
        activation="relu",
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = Conv1D(
        filters=64,
        kernel_size=kernel_size,
        padding="same",
        kernel_initializer="glorot_uniform",
    )(X)
    X = add([X, X_shortcut])

    X = Activation("relu")(X)

    X = GlobalAveragePooling1D()(X)

    X = Dense(units=256, activation="relu", kernel_initializer="he_normal")(X)
    X = Dropout(rate=0.5)(X)

    X = Dense(output_shp, activation="softmax", kernel_initializer="he_normal")(X)

    model = Model(inputs=X_input, outputs=X)

    if verbose:
        model.summary()

    return model


def get_RMLConvNet(input_shp, output_shp, verbose=False):
    """Generate RMLConvNet as defined in O'Shea et Al., Convolutional radio
    modulation recognition networks, 2016
    the implementation is an adaptation of
     https://github.com/radioML/examples/blob/master/modulation_recognition/RML2016.10a_VTCNN2_example.ipynb

    Arguments:
    input_shp (list): shape of the input data [signal_length,2], batch is omitted
    output_shp (list): shape of the output data [n_classes]
    verbose (bool): set verbosity
    """

    dr = 0.5

    model = Sequential()
    model.add(Reshape(input_shp + [1], input_shape=input_shp))

    model.add(ZeroPadding2D((2, 0), data_format="channels_last"))
    model.add(
        Convolution2D(
            256,
            (3, 1),
            padding="valid",
            activation="relu",
            kernel_initializer="glorot_uniform",
            data_format="channels_last",
        )
    )
    model.add(Dropout(dr))

    model.add(ZeroPadding2D((2, 0), data_format="channels_last"))
    model.add(
        Convolution2D(
            80,
            (3, 2),
            padding="valid",
            activation="relu",
            kernel_initializer="glorot_uniform",
            data_format="channels_last",
        )
    )
    model.add(Dropout(dr))

    model.add(Flatten())
    model.add(Dense(256, activation="relu", kernel_initializer="he_normal"))
    model.add(Dropout(dr))
    model.add(Dense(output_shp, kernel_initializer="he_normal", activation="softmax"))

    if verbose:
        model.summary()

    return model


def get_RMLCNNVGG(input_shp, output_shp, verbose=False):
    """Generate RML CNN/VGG  as defined in O'Shea et Al., Over-the-Air Deep Learning
        Based Radio Signal Classification,  2018. The implementation is an adaptation of
        https://github.com/leena201818/radioml/blob/master/rmlmodels/VGGLikeModel.py

    Arguments:
        input_shp (list): shape of the input data [signal_length,2], batch is omitted
        output_shp (list): shape of the output data [n_classes]
        verbose (bool): set verbosity
    """

    dr = 0.5
    kernel_size = 7

    model = Sequential()

    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
            input_shape=input_shp,
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))
    model.add(
        Conv1D(
            filters=64,
            kernel_size=kernel_size,
            activation="relu",
            padding="same",
            kernel_initializer="glorot_uniform",
        )
    )
    model.add(MaxPooling1D(strides=2))

    model.add(Flatten())

    model.add(Dense(128, activation="selu", kernel_initializer="he_normal"))
    model.add(Dropout(dr))

    model.add(Dense(128, activation="selu", kernel_initializer="he_normal"))
    model.add(Dropout(dr))

    model.add(Dense(output_shp, activation="softmax", kernel_initializer="he_normal"))

    if verbose:
        model.summary()

    return model


def residual_stack(X, Filters, Seq, max_pool):
    """Auxiliary function to generate RML CNN/VGG  as defined in O'Shea et Al., Over-the-Air Deep Learning
        Based Radio Signal Classification,  2018. The implementation is an adaptation of
        https://github.com/liuzhejun/ResNet-for-Radio-Recognition/blob/master/ResNet_Model.ipynb

    Arguments:
        X (tensor): input
        Filters (int): number of filters
        Seq (str): module name
        max_pool (bool): enable max pooling at the end
    """

    # 1*1 Conv Linear
    X = Convolution2D(
        Filters,
        (1, 1),
        padding="same",
        name=Seq + "_conv1",
        kernel_initializer="glorot_uniform",
        data_format="channels_last",
    )(X)

    # Residual Unit 1
    X_shortcut = X
    X = Convolution2D(
        Filters,
        (3, 2),
        padding="same",
        activation="relu",
        name=Seq + "_conv2",
        kernel_initializer="glorot_uniform",
        data_format="channels_last",
    )(X)

    X = Convolution2D(
        Filters,
        (3, 2),
        padding="same",
        name=Seq + "_conv3",
        kernel_initializer="glorot_uniform",
        data_format="channels_last",
    )(X)

    X = add([X, X_shortcut])
    X = Activation("relu")(X)

    # Residual Unit 2
    X_shortcut = X
    X = Convolution2D(
        Filters,
        (3, 2),
        padding="same",
        activation="relu",
        name=Seq + "_conv4",
        kernel_initializer="glorot_uniform",
        data_format="channels_last",
    )(X)

    X = Convolution2D(
        Filters,
        (3, 2),
        padding="same",
        name=Seq + "_conv5",
        kernel_initializer="glorot_uniform",
        data_format="channels_last",
    )(X)

    X = add([X, X_shortcut])
    X = Activation("relu")(X)

    # MaxPooling
    if max_pool:
        X = MaxPooling2D(
            pool_size=(2, 1),
            strides=(2, 1),
            padding="valid",
            data_format="channels_last",
        )(X)

    return X


def get_RMLResNet(input_shp, output_shp, verbose=False):
    """Generate RML Residual Network  as defined in O'Shea et Al., Over-the-Air Deep Learning
        Based Radio Signal Classification,  2018. The implementation is an adaptation of
        https://github.com/liuzhejun/ResNet-for-Radio-Recognition/blob/master/ResNet_Model.ipynb

    Arguments:
        input_shp (list): shape of the input data [signal_length,2], batch is omitted
        output_shp (list): shape of the output data [n_classes]
        verbose (bool): set verbosity
    """

    X_input = Input(input_shp)
    X = Reshape(input_shp + [1], input_shape=input_shp)(X_input)
    # Residual Srack 1
    X = residual_stack(X, 32, "ReStk1", False)  # shape:(1,512,32)
    X = MaxPooling2D(
        pool_size=(2, 2), strides=(2, 1), padding="valid", data_format="channels_last"
    )(X)
    # Residual Srack 2
    X = residual_stack(X, 32, "ReStk2", True)  # shape:(1,256,32)
    # Residual Srack 3
    X = residual_stack(X, 32, "ReStk3", True)  # shape:(1,128,32)
    # Residual Srack 4
    X = residual_stack(X, 32, "ReStk4", True)  # shape:(1,64,32)
    # Residual Srack 5
    X = residual_stack(X, 32, "ReStk5", True)  # shape:(1,32,32)
    # Residual Srack 6
    X = residual_stack(X, 32, "ReStk6", True)  # shape:(1,16,32)

    # Full Con 1
    X = Flatten()(X)
    X = Dense(128, activation="selu", kernel_initializer="he_normal", name="dense1")(X)
    X = AlphaDropout(0.3)(X)
    # Full Con 2
    X = Dense(128, activation="selu", kernel_initializer="he_normal", name="dense2")(X)
    X = AlphaDropout(0.3)(X)
    # Full Con 3
    X = Dense(
        output_shp, kernel_initializer="he_normal", name="dense3", activation="softmax"
    )(X)

    model = Model(inputs=X_input, outputs=X)

    if verbose:
        model.summary()

    return model
