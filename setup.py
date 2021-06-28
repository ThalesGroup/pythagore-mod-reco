# Authors: Thomas Courtat, Helion du Mas des Bourboux
# License: MIT

from setuptools import setup, find_packages

DISTNAME = 'pythagore-mod-reco'
DESCRIPTION = 'Modulation recognition algorithms and evaluation'
LONG_DESCRIPTION = open('README.md').read()
MAINTAINER = 'Helion du Mas des Bourboux & Thomas Courtat'
MAINTAINER_EMAIL = "helion.dumasdesbourboux'at'thalesgroup.com"
URL = 'https://github.com/ThalesGroup/'
LICENSE = 'MIT'
VERSION = '0.0.4'

setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    install_requires=[
        'numpy>=1.19.5',
        'matplotlib>=3.4.2',
        'h5py>=3.1.0',
        'tensorflow>=2.5.0',
        'jupyterlab>=3.0.16',
    ],
    packages=['pythagore_modreco'],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires='>=3.6.9',
)
