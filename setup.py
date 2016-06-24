from setuptools import setup, find_packages

setup(
    name='servant',
    packages=find_packages(exclude=['test', 'examples', 'examples.*']),
    version = '0.1.4',
    description = 'A library for building services',
    author='Brian Zambrano',
    author_email='brianz@clearcareonline.com',
    url='https://github.com/clearcare/servant',
    install_requires=[
        'requests>=2.4.3',
        'schematics==1.1.1',
        'bunch==1.0.1',
    ],
    tests_require=[
        'pytest>=2.6.4',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
    ]
)
