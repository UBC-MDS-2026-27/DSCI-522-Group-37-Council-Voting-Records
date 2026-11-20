# Predicting Unanimous Approval in Vancouver City Council Votes

## Project Overview

This project investigates whether meeting type and year can predict whether a Vancouver City Council vote will be carried unanimously. Using the City of Vancouver's publicly available Council Voting Records, we examine voting patterns and prepare a binary classification dataset for evaluating unanimous approval.

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

The data-cleaning process retains records flagged for further review rather than treating every anomaly as an error. Counts depend on the version of the live dataset retrieved.

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

The Quarto document downloads the dataset, performs cleaning and exploratory analysis, and generates `analysis/council-voting-analysis.html`. A collaborator successfully rendered the report using this command on macOS; reproduction on a fresh machine has not yet been verified.

**4. View the report**

Open `analysis/council-voting-analysis.html` in a web browser.

### Environment Reproducibility

The repository includes `pyproject.toml`, `uv.lock`, and `.python-version` so collaborators can recreate the Python environment with `uv sync`. The local `.venv/` directory should not be committed.

## Analysis and Current Findings

The analysis is documented in `analysis/council-voting-analysis.qmd`. The Quarto report creates a vote-level dataset, defines the binary target `is_unanimous`, and splits the votes into 80% training and 20% test data using a stratified random split with `random_state=123`. The split is performed at the council-vote level so individual councillor records for the same decision do not appear in both sets.

Exploratory analysis of the **training data** reports:

- **70.9%** of council votes were carried unanimously.
- Unanimity rates differed by meeting type: **76.8%** for Regular Council meetings, **62.8%** for Policy & Strategic Priorities meetings, and **57.6%** for Special Council meetings.
- Unanimity rates also varied by year. The report records **81.5%** in 2023, **85.4%** in 2024, **79.0%** in 2025, and **68.0%** in the partial 2026 data.

These are descriptive observations from the training set, not evidence that meeting type or year causes changes in voting outcomes. Some meeting types have small sample sizes, and the 2026 data does not cover a full year.

**Current analysis status:** The Quarto source currently documents data preparation, splitting, and exploratory analysis. It does not yet report completed baseline-versus-classifier evaluation metrics or final predictive conclusions. The report's Summary also still contains an editorial placeholder that must be resolved before final submission.

A random historical train/test split would evaluate generalization to held-out historical votes, not necessarily the ability to forecast future council decisions.

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
- `CONTRIBUTING.md`: contribution guidelines file (currently empty on `main`)
- `CODE_OF_CONDUCT.md`: code of conduct file (currently empty on `main`)

## Contributors

Developed by Group 37 for DSCI 522: Data Science Workflows in the University of British Columbia's Master of Data Science program.

- Adnan Ali Syed
- Chloe Surback
- Sam Xu
- Priyanka Sodhi

## License

The repository currently contains an [MIT License](LICENSE). A separate Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license for the written report has been proposed but is not yet reflected in the merged license file. Refer to the current repository license and any subsequently merged license updates.
