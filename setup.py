from setuptools import setup

setup(
    name='smartsearch',
    version='1.0',
    install_requires=[
        'Flask==0.12.2',
        'flask-restplus==0.10.1',
        'marshmallow==2.15.0',
        'us==1.0.0',
        'spacy==2.0.11',
        'aiohttp==3.0.9',
        'requests==2.18.4'
    ],
    url='https://github.com/joshsticks/Capstone',
    license='MIT',
    author='Jonathan Cary, Austin Green, Brandon Watts',
    author_email='caryjb@mymail.vcu.edu, greenaa2@mymail.vcu.edu, wattsbc2@mymail.vcu.edu',
    description='Natural Processing API allowing for Natural Language Search'
)
