from setuptools import setup, find_packages

setup(
    name='servant',
    packages=find_packages(exclude=['test', 'examples', 'examples.*']),
    version = '0.0.4',
    description = 'A library for building services',
    author='Brian Zambrano',
    author_email='brianz@gmail.com',
    url='https://github.com/brianz/servant',
    install_requires=[
        'requests>=2.4.3',
        'schematics>=1.0-0',
        'six>=1.8.0',
        'xmltodict>=0.9.0',
    ],
    tests_require=[
        'pytest>=2.6.4',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
    ]
)
