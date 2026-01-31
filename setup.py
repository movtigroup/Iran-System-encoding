from setuptools import setup, find_packages, Extension
import os

# Optional C Extension
ext_modules = []
if os.name != 'nt': # Simplify for Linux/macOS
    ext_modules = [
        Extension(
            'iran_encoding.libiransystem',
            sources=['iran_encoding/iran_system.c'],
            include_dirs=['iran_encoding'],
        )
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iran-encoding",
    version="1.2.0",
    author="Jules",
    author_email="jules@example.com",
    description="High-performance Iran System visual encoding converter (Unicode <-> IranSystem)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/iran-encoding",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
    install_requires=[], # No dependencies!
    ext_modules=ext_modules,
)
