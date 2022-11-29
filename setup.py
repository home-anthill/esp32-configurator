from setuptools import setup

setup(
    name='esp32-configurator',
    version='1.0.0',
    packages=['src'],
    entry_points={
        'console_scripts': [
            'esp32-configurator = src.__main__:main'
        ]
    })
