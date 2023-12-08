import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.1"

REPO_NAME = "kidney-disease-classification-DL-MLOPS"
AUTHOOR_NAME = "Sadhin"
SRC_REPO = "kidneyDiseaseClassification"
AUTHOR_EMAIL = "sadhin.aiub.cse@gmail.com"

setuptools.setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Kidney Disease classification in Deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/sadhiin/kidney-disease-classification-DL-MLOPS",
    project_urls={
        "Bug Tracker": f"https://github.com/sadhiin/kidney-disease-classification-DL-MLOPS/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9"
)
