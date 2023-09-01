from setuptools import setup, find_packages


setup(
   name='wmul-nocodb',
   version='2.0.1',
   author='Michael Stanley',
   author_email='stanley50@marshall.edu',
   packages=find_packages(),
   license='MIT',
   url='https://github.com/MikeTheHammer/wmul-python-nocodb',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='A package to use NocoDB API in a simple way. A fork of https://github.com/elchicodepython/python-nocodb',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "requests>=2.0",
   ],
)
