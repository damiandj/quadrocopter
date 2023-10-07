import os

from setuptools import setup, find_packages

try:
    tag = os.environ['CI_COMMIT_TAG']
except KeyError:
    tag = "0.1.0"

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='quadrocopter',
    version=tag,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    keywords='',
    packages=find_packages(exclude=['tests', 'assets']),
    install_requires=install_requires,
    dependency_links=[],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'find_path=quadrocopter.main:main',
            'find_path_gui=quadrocopter.main_gui:main',
        ]
    }
)
