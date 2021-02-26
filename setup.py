import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioruz",
    version="0.8.0",
    author="Arseny Mitin",
    author_email="mitinarseny@gmail.com",
    description="Async HSE RUZ API client for Python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mitinarseny/aioruz",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp==3.7.4',
        'asyncio==3.4.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
