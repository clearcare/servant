from setuptools import setup, find_packages

setup(
    name = 'calculator_service',
    packages=find_packages(),
    version = '1.0',
    description = 'Example application with Servant',
    author='Brian Zambrano',
    author_email='brianz@gmail.com',
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
