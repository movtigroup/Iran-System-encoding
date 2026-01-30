import os
from setuptools import setup, find_packages

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = ["setuptools>=65.0.0"]

setup(
    name="iran-encoding",
    version="1.1.0",
    author="Iran System encoding",
    author_email="Iran-System-encoding@movtigroup.ir",
    description="Professional Iran System encoding library with Persian/English support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/movtigroup/Iran-System-encoding",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "iran-encoding=iran_encoding.cli:main",
        ],
    },
    keywords=["persian", "farsi", "encoding", "iran-system", "text-processing"],
    project_urls={
        "Bug Reports": "https://github.com/movtigroup/Iran-System-encoding/issues",
        "Source": "https://github.com/movtigroup/Iran-System-encoding",
    },
)