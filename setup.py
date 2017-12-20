from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nrtree',
    version='0.1',
    license='MIT',
    packages=['nrtree'],
    install_requires=requirements
)
