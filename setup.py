from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
     name='xchg',
     version='0.0.3',
     description='Simulator of a currency exchange.',
     long_description=long_description,
     long_description_content_type='text/markdown',
     author='Sergei Bondarenko',
     author_email='sergei@bondarenko.xyz',
     url='https://github.com/sergei-bondarenko/xchg',
     license='Unlicense',
     packages=['xchg'],
     install_requires=[
         'pandas',
         'poloniex',
         'numpy'
     ],
     entry_points={
         'console_scripts': ['download_sample=xchg.download_sample:_main'],
     }
)
