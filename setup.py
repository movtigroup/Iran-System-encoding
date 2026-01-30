from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iran-encoding",
    version="0.2.3",
    author="Jules",
    author_email="jules@movtigroup.ir",
    description="Two-stage encoding for Persian text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/movtigroup/Iran-System-encoding",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.6",
    install_requires=[
        "arabic_reshaper",
        "python-bidi",
    ],
    entry_points={
        "console_scripts": [
            "iran-encoding=iran_encoding.cli:main",
        ],
    },
)