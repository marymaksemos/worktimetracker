from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='WorkTimeTracker',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'worktimetracker=src.main:main_menu',
        ],
    },
    install_requires=requirements,
)
