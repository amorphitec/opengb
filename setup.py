from setuptools import setup, find_packages

setup(
    name='opengb',
    version='0.15.0',
    author='re:3D',
    author_email='support@re3D.org',
    description='OpenGB printer control.',
    long_description=open('README.md').read(),
    license='LICENSE.txt',
    packages=find_packages(),
    url='http://www.re3d.org/',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'opengb = opengb.server:main',
        ]
    },
    install_requires=[
        'pyserial>=2.7,<3',
        'tornado>=4.2.1,<5',
        'peewee>=2.6.3,<3',
        'json-rpc>=1.10.2,<2',
    ],
    tests_require=[
        'mock>-1.8.1,<2',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
