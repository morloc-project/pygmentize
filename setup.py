from setuptools import setup, find_packages

setup(
    name='morloclexer',
    version='0.1.0',
    description='Pygments lexer for the Morloc language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Zebulun Arendsee',
    author_email='z@morloc.io',
    url='https://github.com/morloc-project/pygmentize',
    license='BSD-3-Clause',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'pygments',
    ],
    entry_points={
        'pygments.lexers': [
            'morloclexer = morloclexer.lexer:MorlocLexer',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='pygments lexer morloc syntax highlighting',
)
