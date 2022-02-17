from setuptools import setup, find_packages

setup(
    name='etest',
    version='1.0',
    packages=find_packages(),
    install_requites=[
        'pytest==4.6.11'
    ],
    include_package_data=True,
    package_data={
        '': ['*.*']
    },
    entry_points={
        'console_scripts': ['etest=etest.parser:parse']
    }
)