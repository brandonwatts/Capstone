from setuptools import setup

setup(
    name='smartsearch',
    version='1.0',
    packages=['smartsearch'],
    install_requires=[
        'Flask==0.12.2',
        'flask-restplus==0.10.1',
        'marshmallow==2.14.0',
        'us==1.0.0',
        'spacy==2.0.6'
    ],
    package_dir={'': 'smartsearch'},
    url='https://github.com/joshsticks/Capstone',
    license='MIT',
    author='Jonathan Cary, Austin Green, Brandon Watts',
    author_email='caryjb@mymail.vcu.edu, greenaa2@mymail.vcu.edu, wattsbc2@mymail.vcu.edu',
    description='Natural Processing API allowing for Natural Language Search'
)
