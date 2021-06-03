# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in jciw/__init__.py
from jciw import __version__ as version

setup(
	name='jciw',
	version=version,
	description='Custom app',
	author='FInByz Tech Pvt Ltd',
	author_email='info@finbyz.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
