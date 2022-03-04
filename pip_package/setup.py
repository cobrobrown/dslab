import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='example0934',
    version='0.2.0',    
    description='A example Python package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cobrobrown/dslab/pip_package/example0934",
    author='Conner Brown',
    author_email='cobrobrown@gmail.com',
    license='BSD 2-clause',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)