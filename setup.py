import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Parse version from _version.py in package directory
# See https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version
version = {}
with open("src/alfred3_scheduler/_version.py") as f:
    exec(f.read(), version)

setuptools.setup(
    name="alfred3_scheduler",
    version=version["__version__"],
    author="Johannes Brachem, Christian Treffenstädt",
    author_email="brachem@uni-goettingen.de",
    description="Organize study appointments with alfred3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jobrachem/alfred3_scheduler",
    packages=setuptools.find_packages("src"),
    package_data={
        "alfred3_scheduler": [
            "templates/html/*",
            "templates/js/*",
            "static/*"
        ]
    },
    package_dir={"": "src"},
    install_requires=[
        "alfred3>=2.0",
        "bleach>=3.2.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
