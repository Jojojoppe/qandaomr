from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='omr',
    version='1.1',
    description='Python and OpenCV OMR (optical mark recognition)',
    long_description=long_description,
    author='Joppe Blondel',
    author_email='joppe@blondel.nl',
    packages=['omr'],
    licence='GPLv3',
    install_requires=['opencv-python', 'numpy', 'argparse', 'zxing'],
    scripts=['scripts/omr']
)
