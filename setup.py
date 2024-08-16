import setuptools

with open('README.md') as fp:
    long_description = fp.read()

setuptools.setup(
    name = 'pyfdec',
    version = '1.0.0',
    url = 'https://github.com/bucccket/PyFdec',
    author = 'bucccket',
    author_email = '',
    license = 'GPL-3.0',
    description = 'A libary for reading and writing to SWF files',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    py_modules = [
        'pyfdec',
    ],
)