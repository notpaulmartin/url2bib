from setuptools import setup, find_packages

readme = open('README.md','r')
README_TEXT = readme.read()
readme.close()

setup(
    name="url2bib",
    version="0.1.0",
    scripts=["url2bib/bin/url2bib"],
    long_description = README_TEXT,
    install_requires=["requests", "re", "bibtexparser", "argparse"],
    include_package_data=True,
    license="GNU GPLv3",
    description="Given a url returns a bibtex, uses publication if available",
    author="Paul Martin",
    author_email="pmartin@skiff.com",
    keywords=["bibtex", "science", "scientific-journals", "crossref", "doi"],

    classifiers=[
        "License :: OSI Approved :: GNU GPLv3 License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "url2bib"},
    url="https://github.com/notpaulmartin/url2bib"
)
