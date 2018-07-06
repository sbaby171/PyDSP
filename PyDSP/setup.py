import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDSP",
    version="0.0.1",
    author="Max Sbabo",
    author_email="",
    description="A DSP tool package for python",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/sbaby171/PyDSP",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)

