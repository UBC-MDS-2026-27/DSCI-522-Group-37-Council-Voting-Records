# Predicting Unanimous Approval in Vancouver City Council Votes

**Authors:** Adnan Ali Syed, Chloe Surbeck, Priyanka Sodhi, and Sam Xu (Group 37, UBC Master of Data Science — DSCI 522)

## Summary

This project asks whether meeting type and calendar year can predict if a Vancouver City Council vote will be carried unanimously. Using 7,665 distinct council votes from the City of Vancouver Open Data Portal (April 2016 to October 2026), we compared a majority-class dummy classifier against unweighted and class-balanced logistic regression models using five-fold cross-validation. On the held-out test set, our selected balanced logistic regression model achieved an Area Under the Receiver Operating Characteristic Curve (ROC-AUC) of 0.650 and a balanced accuracy of 0.601, outperforming the majority-class dummy benchmark on the same test set (0.500 on both metrics) despite lower overall accuracy (0.573 versus 0.709). These findings show that institutional context such as meeting forum and year carries modest predictive signal, though relying solely on metadata without motion text limits overall accuracy and reflects historical patterns rather than future forecasting.

## Published Report

You can read the full rendered analysis, including exploratory visualizations, model diagnostics, and discussion, on GitHub Pages: [Vancouver City Council Voting Analysis Report](https://ubc-mds-2026-27.github.io/DSCI-522-Group-37-Council-Voting-Records/).

## How to Run the Analysis

To reproduce the analysis from scratch, you only need [Git](https://git-scm.com/), [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running), and an internet connection to download the public dataset.

First, clone the repository and move into the project folder:

```bash
git clone https://github.com/UBC-MDS-2026-27/DSCI-522-Group-37-Council-Voting-Records.git
cd DSCI-522-Group-37-Council-Voting-Records
```

Next, make sure you have an SSH key at `~/.ssh/id_ed25519.pub`. If you do not already have one, generate it now and press Enter at each prompt:

```bash
ssh-keygen -t ed25519
```

Skipping this step causes Docker to create an empty folder named `~/.ssh/id_ed25519.pub`, which will block SSH connections until that folder is deleted and a real key is generated.

Download the published Docker image for this project:

```bash
docker compose pull
```

Render the Quarto report inside the container:

```bash
docker compose run --rm analysis-env uv run quarto render analysis/council-voting-analysis.qmd
```

This command downloads the raw voting records from the City of Vancouver Open Data Portal, cleans and aggregates the data, runs the classification analysis, and writes the self-contained HTML report to `analysis/council-voting-analysis.html`. Because of the `--rm` flag, the container stops and removes itself automatically as soon as rendering finishes. If you instead start a background container with `docker compose up -d`, stop and remove it when you are done with `docker compose down`.

Once rendering completes, open `analysis/council-voting-analysis.html` in your web browser to view the report. If you want to modify the project, work interactively inside the container, or contribute changes, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Dependencies

Running the analysis locally requires Git and Docker Desktop. Inside the container, the project uses Ubuntu Linux (`rocker/r-ver:4.6.2`), Quarto `1.11.9`, and Python `3.14` with packages managed and pinned via `uv`. All system and Python dependencies are defined in [Dockerfile](Dockerfile), [pyproject.toml](pyproject.toml), and [uv.lock](uv.lock).

## Licenses

This repository uses the MIT License for all software and code, and the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license for the written report and documentation. Full license texts are provided in [LICENSE.md](LICENSE.md).

## AI Use Statement

Our team used generative AI tools (ChatGPT and Google Gemini) to help brainstorm and refine documentation wording, troubleshoot Docker and Quarto formatting issues, and check our prose for clarity, grammar, and consistency with the reported metrics. All code, analysis decisions, pull requests, and reviews were completed and verified by human team members, who take full responsibility for the submitted work. Example prompts we used include:

- *"Check our Quarto report prose to make sure no code-style variable names appear in text and all acronyms are spelled out on first use."*
- *"Help troubleshoot why `ssh` into our Docker container returns `Permission denied (publickey)` on Windows Docker Desktop."*
- *"Tighten this Results and Discussion draft so it is more concise while keeping all exact test-set metrics."*