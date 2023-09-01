from setuptools import setup

setup(
    name='shmup',
    version='0.01',
    author='David Perez',
    author_email='david.5697.9@gmail.com',
    packages=['shmup'],
    install_requires = ['pygame'],
    entry_points =  {
        "consoles_scripts":[
            'shmup = shmup.__main__:main'
            ]
    }   
)