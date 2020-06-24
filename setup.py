from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
     name='xchg',
     version='0.0.1',
     description='Simulator of a currency exchange.',
     long_description=long_description,
     long_description_content_type='text/markdown',
     author='Sergei Bondarenko',
     author_email='sergei@bondarenko.xyz',
     url='https://github.com/sergei-bondarenko/xchg',
     packages=['xchg'],
     install_requires=['pandas', 'poloniex', 'numpy', 'pytest', 'pytest-pep8'],
     entry_points={
       'console_scripts': ['download_sample=xchg.download_sample:main'],
     }
)
