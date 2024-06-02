from setuptools import setup, find_packages

# Read the contents of the README file
with open('README.md', 'r') as f:
    README = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='lazy_crawler',
    version='0.13',
    description='Lazy Crawler is a Python package that simplifies web scraping tasks. It builds upon Scrapy, a powerful web crawling and scraping framework, providing additional utilities and features for easier data extraction. With Lazy Crawler, you can quickly set up and deploy web scraping projects, saving time and effort.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Pradip-p/lazy-py-crawler',
    author='Pradip Thapa',
    author_email='thapapradip542@gmail.com',
    license='public',
    package_data={
        '': ['*.ini', '*.cfg'],
    },
    include_package_data=True,
    packages=find_packages(exclude=("deploy",)),
    install_requires=requirements,
    zip_safe=False
)
