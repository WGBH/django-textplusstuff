# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-textplusstuff',
    packages=find_packages(exclude=['tests*', 'docs*']),
    version='0.7.1',
    author='Jonathan Ellenberger et al',
    author_email='jay_thompson@wgbh.org',
    url='http://github.com/WGBH/django-textplusstuff/',
    license='MIT License, see LICENSE',
    description=(
        "A django field that makes it easy to intersperse 'stuff' "
        "into blocks of text."
    ),
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=[
        'beautifulsoup4==4.4.0',
        'djangorestframework>=2.4.8',
        'markdown2>=2.3.0',
    ],
    package_data={
        'textplusstuff': [
            'static/textplusstuff/darkly/*.css',
            'static/textplusstuff/fonts/*.*',
            'templates/textplusstuff/*.html',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Markup',
        'Development Status :: 4 - Beta',
    ]
)
