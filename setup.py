from setuptools import setup
setup(
    name='greenview',
    version='0.1.3',
    description='Python Library for reading data from Greenview web service',
    author='Graeme Stuart',
    author_email='ggstuart@gmail.com',
    packages = ['greenview'],
    package_dir = {'': 'lib'},
    url='https://github.com/ggstuart/greenview',
    install_requires=['numpy'],
)
