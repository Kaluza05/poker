from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='poker_server',
    version='0.3',
    url='https://github.com/Kaluza05/poker',
    author='Kamil Kałużny',
    packages=find_packages(),
    install_requires=requirements
)
