import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-bridgekeeper',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A private beta app for Django.',
    long_description=README,
    url='https://www.github.com/brettstil/django-bridgekeeper',
    author='brettstil',
    author_email='brettstil@brettstil.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
    install_requires=[
        'Django>=1.10',
        'shortuuid>=0.5',
    ],
)
