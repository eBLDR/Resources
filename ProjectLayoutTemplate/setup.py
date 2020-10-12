import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='example_pkg',
    version='0.0.1',
    author='Example Author',
    author_email='author@example.com',
    description='A small example package',
    log_description=readme(),  # Project's `homepage`
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/example-project',
    packages=setuptools.find_packages(),
    install_requires=['package_dependency'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    entry_points={
        'console_scripts': [
            'mycmdlineoption = mymodule:main',
        ]
    }
)
