# pythagore-mod-reco
Modulation recognition AI algorithms benchmark.
This project contains a Jupyter Notebook for the interactive benchmark, deep learning networks and a few utility functions gathered into a package. 

## Package to run modulation recognition on raw I/Q radio samples

The acompagning paper is: "A light neural network for modulation detection under impairments, T. Courtat, H. du Mas des Bourboux, 2021, in prep."
submitted to the "2021 International Symposium on Networks, Computers and Communications (ISNCC'21)".
(http://www.isncc-conf.org/)

## Setup
The package requires Python >=3.7. 

It has been tested on Nvidia GPU with cuda 10.2.

### Install package and dependencies

The package installation is as simple as
```bash
cd <project_folder>
pip3 install -U .
```

If you only need to install dependencies you can go with
```bash
python -m pip install -r requirements.txt
```

### Get data
The trainning and testing of algorithms can be performed on several datasets:

- The pythagore-mod-reco AugMod dataset as presented in our article:

```bash 
wget https://augmod.blob.core.windows.net/augmod/augmod.zip
unzip augmod.zip
``` 
- RML 2016 datasets from DeepSig:
```bash
wget https://opendata.deepsig.io/datasets/2016.04/2016.04C.multisnr.tar.bz2?__hstc=233546881.9c91e0549f9b6bfce6708a49c211c1c9.1614872457734.1614872457734.1614872457734.1&__hssc=233546881.1.1614872457735&__hsfp=1843090487
wget https://opendata.deepsig.io/datasets/2016.10/RML2016.10b.tar.bz2?__hstc=233546881.9c91e0549f9b6bfce6708a49c211c1c9.1614872457734.1614872457734.1614872457734.1&__hssc=233546881.1.1614872457735&__hsfp=1843090487
wget https://opendata.deepsig.io/datasets/2016.10/RML2016.10a.tar.bz2?__hstc=233546881.9c91e0549f9b6bfce6708a49c211c1c9.1614872457734.1614872457734.1614872457734.1&__hssc=233546881.1.1614872457735&__hsfp=1843090487
```

- RML 2018 dataset from DeepSig

To get RadioML2018.01A  you should connect to https://www.deepsig.ai/datasets

Please update path `data_path` and `log_path` in `jupyter/train-test-modulationreco.ipynb` to where data are located and to where you want to store log files

## Run

- Train and test the different networks on each datasets running `jupyter/train-test-modulationreco.ipynb`

## Source

- The implementation of RML-ConvNet is found at https://github.com/radioML/examples/blob/master/modulation_recognition/RML2016.10a_VTCNN2_example.ipynb
- The implementation of RML-CNN/VGG is found at https://github.com/leena201818/radioml/blob/master/rmlmodels/VGGLikeModel.py
- The implementation of RML-ResNet is found at https://github.com/liuzhejun/ResNet-for-Radio-Recognition/blob/master/ResNet_Model.ipynb

## Citing

- Please cite "A light neural network for modulation detection under impairments, T. Courtat, H. du Mas des Bourboux, 2021, in prep."
if you are using the AugMod dataset or Mod-LCNN or Mod-LRCNN networks
```bash
@ARTICLE{CourtatduMasdesBourBoux2021,
       author = {{Courtat}, Thomas and {du Mas des Bourboux}, H{\'e}lion},
        title = "{A light neural network for modulation detection under impairments}",
      journal = {inprep},
     keywords = {Computer Science - Machine Learning, Electrical Engineering and Systems Science - Signal Processing, Statistics - Machine Learning},
         year = 2021,
        month = april,
          eid = {},
        pages = {},
archivePrefix = {},
       eprint = {},
 primaryClass = {},
       adsurl = {},
      adsnote = {}
}
```
- Please visit https://www.deepsig.ai/datasets to see how to cite RadioML datasets and networks

## License

- This repository is licensed under the terms of the MIT License (see the file LICENSE).
