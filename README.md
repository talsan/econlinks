# Economic Linkages: A Text-Based Approach
### Creating company peer-groups using topic modelling / clustering on text from quarterly earnings calls and company business descriptions.

Start Here: [`explore_nb.ipynb`](https://github.com/talsan/econlinks/blob/master/explore_nb.ipynb) (jupyter notebook)

Notes:
* conference call data sourced from fool.com (transcript scraping code is [here](https://github.com/talsan/foolcalls))
* that text/data is downloaded from within [`download_transcripts.py`](https://github.com/talsan/econlinks/blob/master/download_transcripts.py)
* downloader draws on various helper modules for aws interaction contained in `utils_athena.py` and `utils_s3.py`
