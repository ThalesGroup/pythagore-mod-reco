# Authors: Thomas Courtat, Hélion du Mas des Bourboux
# License: MIT

from setuptools import setup, find_packages

DISTNAME = 'PyThagore-ModReco'
DESCRIPTION = 'Modulation recognition algorithms and evaluation'
LONG_DESCRIPTION = open('README.md').read()
MAINTAINER = 'Hélion du Mas des Bourboux & Thomas Courtat'
MAINTAINER_EMAIL = "helion.dumasdesbourboux'at'thalesgroup.com"
URL = 'https://github.com/ThalesGroup/'
LICENSE = 'MIT'
VERSION = '0.1.0'

setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    install_requires=[
          'numpy>=1.18.4',
	  'matplotlib>=3.4.1',
          'h5py>=2.10.0',
          'tensorflow==2.2.0',
          'jupyterlab>=3.0.14',
    ],
    packages=['pythagore_modreco'],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
)
