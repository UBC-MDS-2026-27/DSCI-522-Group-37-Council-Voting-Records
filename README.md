# Predicting Unanimous Approval in Vancouver City Council Votes

## Project Overview

This project investigates whether meeting type and year can predict whether a Vancouver City Council vote will be carried unanimously. Using the City of Vancouver's publicly available Council Voting Records, we examine voting patterns and develop a binary classification analysis.

**Research question:** Can meeting type and year predict whether a Vancouver City Council vote will be carried unanimously?

The target is `is_unanimous`: 1 for decisions recorded as "Carried Unanimously", and 0 for decisions recorded as "Carried" or "Lost". The predictors are meeting type and the calendar year extracted from the voting date.

## Dataset and Data Source

Source: [City of Vancouver Open Data Portal — Council Voting Records](https://opendata.vancouver.ca/explore/dataset/council-voting-records/).

The original dataset records individual councillors' votes, including meeting information, dates, councillor names, voting statuses, and decisions. As reported in the team's November 18, 2026 analysis, the cleaned dataset contained 83,805 records from April 2016 to October 2026, representing 7,665 distinct council votes. Counts may change when the source is downloaded again.

The raw CSV is downloaded to `data/raw/council_voting_records.csv`. For modelling, individual councillor records are aggregated to one observation per council vote.

## Data Cleaning and Quality Checks

The data-cleaning workflow in `scripts/clean_data.py`:

1. Converts vote dates and timestamps to datetime values.
2. Validates unique `vote_detail_id` values.
3. Removes redundant councillor-vote records only when voting statuses agree.
4. Flags conflicting councillor-vote statuses, date mismatches, potentially inconsistent decisions, and votes with fewer than 11 recorded councillors.
5. Preserves flagged observations for review instead of automatically discarding them.

In the team's initial cleaning run, 19 redundant records were removed, 3 councillor-vote combinations had conflicting statuses, and 11 council decisions were flagged as potentially inconsistent. These counts describe that run, not necessarily future downloads.

The cleaning script writes:

- `data/processed/council_voting_clean.parquet`: cleaned records
- `data/processed/votes_to_review.csv`: records flagged for review

The Quarto analysis additionally creates `data/processed/council_voting_vote_level.parquet` for modelling.

## Reproducing the Analysis

### Prerequisites

Install:

- [Git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Quarto](https://quarto.org/docs/get-started/)

An internet connection is needed to download the City of Vancouver dataset.

The project uses Python 3.14, specified in `.python-version`. Dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

### Setup and Execution

**1. Clone the repository**

```bash
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-37-Council-Voting-Records.git
cd DSCI-522-Group-37-Council-Voting-Records
```

**2. Set up the Python environment**

```bash
uv sync
```

This creates the project's `.venv/` environment and installs the locked dependencies.

**3. Render the Quarto report**

From the repository root:

```bash
uv run quarto render analysis/council-voting-analysis.qmd
```

The Quarto document contains code to download, clean, and analyse the voting records. Rendering is intended to generate `analysis/council-voting-analysis.html`. This command has not yet been independently tested end-to-end for this README update.

**4. View the report**

Open `analysis/council-voting-analysis.html` in a web browser.

### Environment Reproducibility

The repository includes `pyproject.toml`, `uv.lock`, and `.python-version` so collaborators can recreate the Python environment with `uv sync`. The local `.venv/` directory should not be committed.

## Analysis and Modelling

The Quarto report, `analysis/council-voting-analysis.qmd`, contains the full analysis. It constructs a vote-level dataset, uses an 80/20 stratified training/test split with a fixed random seed, and explores unanimity by meeting type and year.

The modelling workflow evaluates classification approaches against a baseline. Cross-validation scores on training data and scores on a held-out test set are not directly comparable unless the evaluation procedure is aligned. Consult the report for the methods and results; the analysis is still being refined.

The random held-out split assesses performance on historical votes, not necessarily predictions for future years.

## Project Structure

- `analysis/`: Quarto source report and rendered output
- `data/raw/`: original voting records
- `data/processed/`: cleaned data and flagged records
- `notebooks/`: exploratory notebooks
- `scripts/fetch_data.py`: download script
- `scripts/clean_data.py`: cleaning and validation script
- `pyproject.toml`: Python project dependencies
- `uv.lock`: locked dependency versions
- `.python-version`: Python version
- `README.md`: project overview, dataset information, and reproduction instructions
- `CONTRIBUTING.md`: contribution guidelines (pending documentation update)
- `CODE_OF_CONDUCT.md`: contributor conduct guidance (pending documentation update)

## Contributors

Developed by Group 37 for DSCI 522: Data Science Workflows in the University of British Columbia's Master of Data Science program.

- Adnan Ali Syed
- Chloe Surback
- Sam Xu
- Priyanka Sodhi

## License

The project intends to use the MIT License for software and Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) for the written report. The repository's license documentation is being updated; check the merged license file for the applicable terms.
