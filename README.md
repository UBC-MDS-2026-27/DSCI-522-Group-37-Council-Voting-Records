# Predicting Unanimous Approval in Vancouver City Council Votes

## Project Overview

This project investigates whether meeting type and year can predict whether a Vancouver City Council vote will be carried unanimously. Using the City of Vancouver's publicly available Council Voting Records, we examine voting patterns and compare classification models for predicting unanimous approval.

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

## Analysis and Findings

The analysis is documented in `analysis/council-voting-analysis.qmd`. The Quarto report creates a vote-level dataset, defines the binary target `is_unanimous`, and splits the votes into 80% training and 20% test data using a stratified random split with `random_state=123`. The split is performed at the council-vote level so individual councillor records for the same decision do not appear in both sets.

Exploratory analysis of the **training data** reports:

- **70.9%** of council votes were carried unanimously.
- Unanimity rates differed by meeting type: **76.8%** for Regular Council meetings, **62.8%** for Policy & Strategic Priorities meetings, and **57.6%** for Special Council meetings.
- Unanimity rates also varied by year. The report records **81.5%** in 2023, **85.4%** in 2024, **79.0%** in 2025, and **68.0%** in the partial 2026 data.

These are descriptive observations from the training set, not evidence that meeting type or year causes changes in voting outcomes. Some meeting types have small sample sizes, and the 2026 data does not cover a full year.

### Modelling and Evaluation

The completed modelling work is available in Chloe's [analysis PR #7](https://github.com/UBC-MDS-2026-27/DSCI-522-Group-37-Council-Voting-Records/pull/7), which is pending merge into `main`.

The team compared a majority-class `DummyClassifier`, standard logistic regression, and class-weighted logistic regression. Both `meeting_type` and `year` were one-hot encoded within the modelling pipeline. Models were compared using five-fold cross-validation on the training data, with ROC-AUC and balanced accuracy prioritized because approximately 71% of training votes were unanimous.

| Model | CV accuracy | CV balanced accuracy | CV ROC-AUC |
| --- | ---: | ---: | ---: |
| Majority-class dummy | 0.709 | 0.500 | 0.500 |
| Logistic regression | See Table 1 in the report | 0.500 | Approximately 0.636 |
| Balanced logistic regression | 0.579 | 0.598 | 0.637 |

The balanced logistic regression model was selected for final evaluation. On the **held-out test set**, it achieved:

| Test metric | Balanced logistic regression |
| --- | ---: |
| Accuracy | 0.573 |
| Balanced accuracy | 0.601 |
| ROC-AUC | 0.650 |

The report's test-set confusion matrix shows 582 correctly classified unanimous votes, 297 correctly classified non-unanimous votes, 505 unanimous votes classified as non-unanimous, and 149 non-unanimous votes classified as unanimous.

**Important evaluation distinction:** The dummy baseline values shown above come from training-set cross-validation, while the selected model's final values come from the held-out test set. They are not a like-for-like test-set comparison. The cross-validation results provide the appropriate direct model comparison; the test results describe final performance of the selected model.

### Interpretation and Limitations

Meeting type and year show **modest predictive signal**, but they do not reliably determine whether a vote will be unanimous. The fitted model associates Regular Council and certain administrative meeting types, along with 2023–2024, with higher unanimity; Special Council and Policy and Strategic Priorities meetings show lower unanimity.

The analysis uses only meeting type and year, not the content or subject of motions. Its random split evaluates held-out historical decisions rather than future-year forecasting. The dataset also retains flagged anomalous records, some meeting types have limited observations, and 2026 is incomplete. The findings are best treated as exploratory rather than as a basis for automated decisions.

See the [Quarto report in PR #7](https://github.com/UBC-MDS-2026-27/DSCI-522-Group-37-Council-Voting-Records/blob/analysis-2/analysis/council-voting-analysis.qmd) for the full methodology, visualizations, coefficient analysis, and discussion.

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
