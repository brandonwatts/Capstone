from setuptools import setup

setup(
   name='api',
   version='1.0',
   description='VCU Capstone Project',
   packages=['api'],
   install_requires=['flask', 'flask-restplus', 'google-cloud']
)
