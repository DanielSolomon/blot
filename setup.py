import setuptools

with open('requirements.txt', 'r') as reader:
    reqs = reader.read().splitlines()

setuptools.setup(
    name                = 'pyshart',
    version             = '1.0.0',
    url                 = 'http://github.com/DanielSolomon/pyshart',
    author              = 'Daniel Solomon & Divo Kaplan',
    license             = 'MIT',
    packages            = ['pyshart'],
    zip_safe            = False,
    install_requires    = reqs,
)