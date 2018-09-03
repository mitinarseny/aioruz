import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioruz",
    version="0.0.1",
    author="Arseny Mitin",
    author_email="mitinarseny@gmail.com",
    description="Async HSE RUZ API client for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mitinarseny/aioruz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)