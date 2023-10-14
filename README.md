# URL to BibTeX Converter (url2bib)

url2bib is a commandline tool for converting URLs of papers into into BibTeX citations. It tries to use the publication information rather than the arXiv url.

## Example
Here's an example of how to use the script:

```bash
python url2bib.py https://arxiv.org/abs/2006.11477
```

## Prerequisites
Before using this script, make sure you have the following prerequisites installed:

- Python 3.x
- Required Python packages, which can be installed via pip:
  - bibtexparser


## Usage
To use the URL to BibTeX Converter (`url2bib`), follow these steps:

1. Clone this repository to your local machine or download the script.

2. Open your terminal/command prompt and navigate to the directory containing the script.

3. Run the script with the following command:
    ```bash
    python url2bib.py [URL]
    ```
    Replace [URL] with the URL of the webpage you want to extract BibTeX citations from.

4. The script will retrieve BibTeX entries corresponding to the DOIs found in the webpage and print the resulting BibTeX citation to the console.

## Features
- Extracts DOIs from URLs and retrieves BibTeX citations for those DOIs.
- Searches for publications of the paper.
- Generates a BibTeX entry with a unified ID in the format `{firstAuthorSurname}_{year}_{titleFirstWord}`.

## Contributing
Contributions to this project are welcome. If you have any suggestions or want to report issues, please open an issue or submit a pull request.

## License
This project is under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0) license.

## Acknowledgments
This script uses the `bibtexparser` library for parsing and generating BibTeX entries.
It also relies on external data sources such as doi.org and dblp.org to fetch BibTeX entries.

## Disclaimer
This script is provided as-is, and the accuracy of the generated BibTeX entries depends on the availability and quality of external data sources. Always double-check and edit citations as needed for your research papers and publications.

Happy citing with `url2bib`!
