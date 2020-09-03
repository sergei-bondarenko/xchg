import codecs
import os.path
from setuptools import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError('Unable to find version string.')


PACKAGE_NAME = 'xchg'

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version=get_version(f"{PACKAGE_NAME}/__init__.py"),
    description='Simulator of a currency exchange.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sergei Bondarenko',
    author_email='sergei@bondarenko.xyz',
    url=f"https://github.com/sergei-bondarenko/{PACKAGE_NAME}",
    license='Unlicense',
    packages=[PACKAGE_NAME],
    install_requires=[
        'pandas',
        'poloniex',
        'numpy'
    ],
    entry_points={
        'console_scripts':
            [f"download_candles={PACKAGE_NAME}.download_candles:_main"],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
