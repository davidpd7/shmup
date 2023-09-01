from setuptools import setup

setup(
    name='shmup',
    version='0.01',
    author='David Perez',
    author_email='david.perez@cubematch.com',
    packages=['shmup'],
    install_requires = ['pygame'],
    entry_points =  {
        "consoles_scripts":[
            'shmup = shmup.__main__:main'
            ]
    }   
)