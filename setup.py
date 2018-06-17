import setuptools

with open('requirements.txt', 'rb') as reader:
    reqs = reader.read().splitlines()

setuptools.setup(
    name                = 'blot',
    version             = '1.0.0',
    url                 = 'http://github.com/DanielSolomon/blot',
    author              = 'Daniel Solomon & Divo Kaplan',
    license             = 'MIT',
    packages            = ['blot'],
    zip_safe            = False,
    install_requires    = reqs,
)