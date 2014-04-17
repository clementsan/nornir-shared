'''
Created on Aug 30, 2013

@author: u0490822
'''

from ez_setup import use_setuptools


if __name__ == '__main__':
    use_setuptools()

    from setuptools import setup

    install_requires = ["six"]

    setup(name='nornir_shared',
          version='1.1.7',
          description="Shared routines for Nornir python packages and scripts",
          author="James Anderson",
          author_email="James.R.Anderson@utah.edu",
          url="https://github.com/jamesra/nornir-shared",
          packages=["nornir_shared"],
          install_requires=install_requires,
          test_suite='test')
