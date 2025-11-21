import re
import pathlib
from setuptools import setup
from setuptools import find_packages

name = "python_etf_db_service"
here = pathlib.Path.absolute(pathlib.Path(__file__).resolve().parent)

with open("README.md", "r") as fh:
    long_description = fh.read()

# get package version
with open(
    pathlib.Path(here, f"src/{name}/__init__.py"), encoding="utf-8"
) as f:
    result = re.search(r'__version__ = ["\']([^"\']+)', f.read())

    if not result:
        raise ValueError(f"Can't find the version in {name}/__init__.py")

    version = result.group(1)

dev_requirements = {"black", "pre-commit"}
api_requirements = {"fastapi", "uvicorn[standard]"}

setup(
    name=name,
    version=version,
    author="Yi Kuang",
    author_email="yikuang5@gmail.com",
    description="Scrape ETFs from ETFDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvxhnat/pyetf-scraper",
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["*tests"]),
    package_data={name: ["data/etfdb.json", "data/user-agents.txt"]},
    python_requires=">=3.7",
    install_requires=[
        "pydantic",
        "requests",
        "bs4",
        "lxml",
        "cloudscraper",
    ],
    extras_require={
        "dev": list(dev_requirements),
        "api": list(api_requirements),
        "all": list(dev_requirements | api_requirements),
    },
    entry_points={
        "console_scripts": [
            "etfdb=python_etf_db_service.cli:main",
        ],
    },
)
