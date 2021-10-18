from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='igqloo',
    version='0.1',
    description='A simple command-line tool for writing GQL queries',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/gerhalt/igqloo',
    author='Josh Mottaz',
    author_email='gerhalt@gmail.com',

    classifiers=[
        # TODO: Add license
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='graphql, gql, cli, queries, development',

    python_requires='>=3.8, <4',
    py_modules = ['igqloo'],
    install_requires=[
        'Click',
        'requests'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'igqloo=igqloo:main',
        ],
    },
)
