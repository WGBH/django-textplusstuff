# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')
    install_requires += [
        'git+https://github.com/eyemyth/django-jsonfield.git#egg=jsonfield',
    ]

setup(
    name='django-textplusstuff',
    packages=find_packages(exclude=['tests*', 'docs*']),
    version='0.7',
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
    install_requires=install_requires,
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
