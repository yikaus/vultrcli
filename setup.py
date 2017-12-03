#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "vucli",
    version = "0.0.3",
    packages = find_packages(),


    include_package_data = True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst','*.js','*.css','*.html','*.jpg',],
        # And include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],

    },

    # metadata for upload to PyPI
    author = "Kevin Yi",
    description = "Vultr VPS cloud CLI console",
    license = "BSD",
    keywords = "cloud CLI REST admin administrator node vultr",
    install_requires=["requests","argparse"],
    extras_require={':sys_platform == "win32"': ['pyreadline']},
    url = "https://github.com/yikaus/vultrcli",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.

    entry_points = {
        'console_scripts': [
            'vucli = vucli.vucli:main',

        ],
    }
)