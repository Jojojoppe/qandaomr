from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='qandaomr',
    version='1.2.3',
    description='Q&A Python and OpenCV OMR (optical mark recognition)',

    author='Joppe Blondel',
    author_email='joppe@blondel.nl',
    download_url='https://github.com/Jojojoppe/qandaomr/archive/v1.2.3.tar.gz',
    url='https://github.com/Jojojoppe/qandaomr',

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

    packages=['qandaomr'],
    licence='GNU General Public License v3 (GPLv3)',
    install_requires=['opencv-python', 'numpy', 'argparse', 'zxing'],
    scripts=['scripts/qandaomr']
)
