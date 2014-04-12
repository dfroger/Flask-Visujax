"""
Flask-Visujax
-------------

Dynamic scientific visualization using Ajax.
"""
from setuptools import setup


setup(
    name='Flask-Visujax',
    version='0.0.1',
    url='https://github.com/dfroger/flask_visujax',
    license='BSD',
    author='David Froger',
    author_email='david.froger@gmail.com',
    description='Dynamic scientific visualization using Ajax.',
    long_description=__doc__,
    packages=['flask_visujax'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Bootstrap',
        'Flask-Sijax',
        'Flask-WTF',
        'beautifulsoup4',
        'numpy',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

