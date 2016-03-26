try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='SmartDashboardLauncher',
    version='1.0',
    description='Launcher that waits for NetworkTables initialization before launching SmartDashboard',
    author='Rishov Sarkar',
    author_email='rishov.s@prhsrobotics.com',
    license='MIT',
    py_modules=['sdlauncher'],
    install_requires=[
        'pynetworktables'
    ]
)
