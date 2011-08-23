from distutils.core import setup
setup(
    name='greenview',
    version='0.1.2',
    description='Python Library for reading data from Greenview web service',
    author='Graeme Stuart',
    author_email='ggstuart@gmail.com',
    packages = ['greenview', 'greenview.examples'],
    package_dir = {'': 'lib'},
    url='https://github.com/ggstuart/greenview',
    requires=['numpy'],
)
