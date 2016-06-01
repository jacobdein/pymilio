"""
Jacob Dein 2016
Pymilio
Author: Jacob Dein
License: MIT
"""


from setuptools import setup, find_packages

setup(	name='Pymilio',
		version='0.1.0',
		description='Python interface to Pumilo database',
		author='Jacob Dein',
		author_email='jake@jacobdein.com',
		url='https://github.com/jacobdein/pymilio',
		packages=find_packages(),
		license='MIT',
		platforms='any',
		classifiers=[
		  'License :: OSI Approved :: MIT License',
		  'Development Status :: 3 - Alpha',
		  'Programming Language :: Python :: 2.7',
		  'Programming Language :: Python :: 3',
		  'Environment :: Console'],
)