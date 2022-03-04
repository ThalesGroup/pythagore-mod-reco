# Authors: Thomas Courtat, Helion du Mas des Bourboux
# License: MIT

from setuptools import setup, find_packages

DISTNAME = "pythagore-modreco"
DESCRIPTION = "Modulation recognition algorithms and evaluation"
LONG_DESCRIPTION = open("README.md").read()
MAINTAINER = "Helion du Mas des Bourboux & Thomas Courtat"
MAINTAINER_EMAIL = "helion.dumasdesbourboux'at'thalesgroup.com"
URL = "https://github.com/ThalesGroup/"
LICENSE = "MIT"

exec(open("pythagore_modreco/_version.py").read())
VERSION = __version__

with open("requirements.txt") as f:
    REQUIRED = f.read().splitlines()

setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    install_requires=REQUIRED,
    packages=["pythagore_modreco"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.9",
)
