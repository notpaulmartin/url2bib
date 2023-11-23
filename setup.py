from setuptools import setup, find_packages

readme = open('README.md','r')
README_TEXT = readme.read()
readme.close()

setup(
    name="url2bib",
    version="0.1.11",
    scripts=["url2bib/bin/url2bib"],
    long_description = README_TEXT,
    install_requires=["requests", "bibtexparser", "urllib3"],
    include_package_data=True,
    license="GNU General Public License v3 (GPLv3)",
    description="Given a url returns a bibtex, uses publication if available",
    author="Paul Martin",
    author_email="pmartin@skiff.com",
    keywords=["bibtex", "science", "scientific-journals", "crossref", "doi"],

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
    package_dir = {"": "url2bib"},
    url="https://github.com/notpaulmartin/url2bib"
)
