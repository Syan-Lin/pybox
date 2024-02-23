from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'A CLI Box Maker in Python'
LONG_DESCRIPTION = 'A CLI Box Maker in Python'

setup(
        name="pyboxmaker",
        version=VERSION,
        author="SyanLin",
        author_email="<lin.siyuan@foxmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['colorama'],
        license='MIT',
        url='https://github.com/Syan-Lin/pyboxmaker',

        keywords=['python', 'box maker'],
        classifiers= [
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)