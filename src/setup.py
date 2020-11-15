import setuptools


setuptools.setup(
    name             = 'pypackager',
    version          = '1.0.0',
    description      = 'Python tool to make a package out of a set of scripts. This package was created by itself.',
    url              = 'https://github.com/madisi98/PyPackager',
    author           = 'Manuel Diez Silva',
    author_email     = 'madisi1998@gmail.com',
    maintainer       = 'Manuel Diez Silva',
    maintainer_email = 'madisi1998@gmail.com',
    packages         = setuptools.find_packages(),
    entry_points     = {
        'console_scripts': [
            'pypackager=pypackager.launcher:launcher'
        ],
    }
)
