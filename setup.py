from setuptools import setup
from k_means_plus_plus import _version

requirements = []

with open("requirements.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            requirements.append(line)

setup(
    name="k-means-plus-plus",
    version=_version.__version__,
    author="Jack Maney",
    author_email="jackmaney@gmail.com",
    description="K-Means++ Clustering for Pandas DataFrames",
    long_description=open("README.md").read(),
    license="MIT",
    url="https://github.com/jackmaney/k-means-plus-plus-pandas",
    packages=["k_means_plus_plus"],
    install_requires=requirements
)
