from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='qandaomr',
    version='1.2',
    description='Q&A Python and OpenCV OMR (optical mark recognition)',
    long_description=long_description,

    author='Joppe Blondel',
    author_email='joppe@blondel.nl',
    download_url='https://github.com/Jojojoppe/qandaomr/archive/v1.2.tar.gz',
    url='https://github.com/Jojojoppe/qandomr',

    keywords = ['OMR', 'Optical Mark Recognition',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
  ],

    packages=['omr'],
    licence='GNU General Public License v3 (GPLv3)',
    install_requires=['opencv-python', 'numpy', 'argparse', 'zxing'],
    scripts=['scripts/qandaomr']
)
