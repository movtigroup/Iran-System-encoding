from setuptools import setup, Extension

# Define the extension module
iran_system_module = Extension(
    'iran_system_ext',
    sources=['iran_encoding/iran_system.c'],
    include_dirs=['iran_encoding/']
)

# Setup configuration
setup(
    name='iran_system_c_extension',
    version='0.2.3',
    description='C extension for Iran System encoding',
    ext_modules=[iran_system_module]
)