from setuptools import setup

setup(
    name='pydab',
    version='0.1.0',
    packages=['dab'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'dab = dab.cli:cli'
        ]
    }
)
