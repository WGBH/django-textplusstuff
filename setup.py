# -*- coding: utf-8 -*-
from distutils.core import setup
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import find_packages
import uuid

setup(
    name='django-textplusstuff',
    packages=find_packages(exclude=['tests*', 'docs*']),
    version='0.9.1',
    author='Jonathan Ellenberger et al',
    author_email='jay_thompson@wgbh.org',
    url='http://github.com/WGBH/django-textplusstuff/',
    license='MIT License, see LICENSE',
    description="A django field that makes it easy to intersperse 'stuff' "
                "into blocks of text.",
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=[
        str(ir.req)
        for ir in parse_requirements('requirements.txt', session=uuid.uuid1())
    ],
    package_data={
        'textplusstuff': [
            'static/textplusstuff/darkly/*.css',
            'static/textplusstuff/fonts/*.*',
            'templates/textplusstuff/*.html'
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup',
        'Development Status :: 4 - Beta'
    ]
)
