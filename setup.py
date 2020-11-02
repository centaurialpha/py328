from glob import glob
from os.path import splitext, basename
from setuptools import setup, find_packages

setup(
    name='py328',
    version='0.1',
    author='Gabriel Acosta',
    author_email='acostadariogabriel@gmail.com',
    description='Interface for Arduino UNO using firmata protocol',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'pyserial',
    ],
    extras_require={
        'testing': [
            'pytest',
        ],
        'dev': [
            'ipython',
        ]
    },
    platform=['any'],
    url='https://github.com/centaurialpha/py328',
    license='GPLv3',
)
