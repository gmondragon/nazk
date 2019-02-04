import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nazk',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/gmondragon/nazk',
    license='GNU General Public License v3.0',
    author='Gabriel Mondragón',
    author_email='gabriel@mondragon.pe',
    description='Get the official exchange rate of the SBS and SUNAT.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas',
        'numpy',
        'lxml'
    ]
)
