# -*- coding: utf-8 -*-
"""Setup for anotes"""

from setuptools import setup, find_packages
NAME = 'Anotes'
DESCRIPTION = "A notes manager"
URL = 'https://github.com/arfs6/'
VERSION = '0.0.1'
AUTHOR = 'Abdulqadir Ahmad'
AUTHOR_EMAIL = 'arfs6.mail@gmail.com'
with open('README.md', 'r', encoding='utf-8') as fileObj:
    LONG_DESCRIPTION = fileObj.read()

INSTALL_REQUIRES = [
        'urwid',
        'peewee',
        'setuptools',
        ]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'anotes = anotes.cli:run',
        ],
    },
    install_requires=INSTALL_REQUIRES,
    license='gpl2',
    package_data={'anotes': ['templates/*.html']},
)
