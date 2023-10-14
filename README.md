# URL to BibTeX Converter (url2bib)

This Python script, named "url2bib," is a utility for converting URLs containing Digital Object Identifiers (DOIs) into BibTeX citations. It is designed to help researchers and academics easily generate BibTeX entries for online resources when writing LaTeX documents.

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

## Example
Here's an example of how to use the script:

```bash
python url2bib.py https://arxiv.org/abs/2006.11477
```

## Features
- Extracts DOIs from URLs and retrieves BibTeX citations for those DOIs.
- Chooses the best publication (not informal) when multiple BibTeX entries are available.
- Generates a BibTeX entry with a unified ID in the format `{firstAuthorSurname}_{year}_{titleFirstWord}`.
- Cleans up BibTeX entries, removing unnecessary whitespace.


## Contributing
Contributions to this project are welcome. If you have any suggestions or want to report issues, please open an issue or submit a pull request.

## Acknowledgments
This script uses the `bibtexparser` library for parsing and generating BibTeX entries.
It also relies on external data sources such as doi.org and dblp.org to fetch BibTeX entries.

## Disclaimer
This script is provided as-is, and the accuracy of the generated BibTeX entries depends on the availability and quality of external data sources. Always double-check and edit citations as needed for your research papers and publications.

Happy citing with `url2bib`!
