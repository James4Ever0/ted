from setuptools import setup, find_packages


setup(
    name='ted-editor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'textual>=0.1.18',
    ],
    entry_points={
        'console_scripts': [
            'ted = ted.cli:main',
        ],
    },
    author='James Brown',
    author_email='randomvoidmail@foxmail.com',
    description='Terminal Text Editor with TUI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/James4Ever0/ted',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'ted': ['*.css'],
    },
)