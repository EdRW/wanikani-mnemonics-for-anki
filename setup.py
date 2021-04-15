# pyright: basic
from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['aqt~=2.1.35']

setup(
    name='wk_mnemonics',
    version='0.1',
    python_requires='~=3.8.5',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description=
    'This package is development of the wanikani mnemonics add-on for anki.',
)