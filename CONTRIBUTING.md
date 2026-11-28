# Contributing Guidelines

Thank you for contributing to this project! These guidelines explain how to develop inside the project's Docker container, update dependencies, republish the report, and submit changes through GitHub.

## Getting Started

Before developing, follow the initial setup steps in [README.md](README.md) to clone the repository, generate an SSH key (`~/.ssh/id_ed25519.pub`), and download the Docker image (`docker compose pull`).

## Working in the Container with Positron over SSH

All code changes, package updates, and report renders should be done inside the project's Docker container so everyone works in the exact same environment.

1. Install [Positron](https://positron.posit.co/) (with the Remote-SSH extension enabled).
2. Make sure your global Git name and email are configured on your computer so commits inside the container are attributed to you:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your-email@example.com"
   ```
3. Start the container in the background from the repository root:
   ```bash
   docker compose up -d
   ```
4. Add a host entry to your local `~/.ssh/config` (if you do not already have one for port `2222`):
   ```text
   Host docker-uv-renv
     HostName localhost
     Port 2222
     User root
     IdentityFile ~/.ssh/id_ed25519
     StrictHostKeyChecking no
     UserKnownHostsFile /dev/null
   ```
5. In Positron, click the Remote (`><`) icon in the bottom-left corner, choose **Connect to Host...**, and select `docker-uv-renv` (choose **Linux** if prompted).
6. Open the mounted project directory by clicking **Open Folder** and entering `/workspace`. Any file you edit in `/workspace` updates directly on your computer.
7. Select the container's Python interpreter at `/opt/venv/bin/python` (do **not** select `/workspace/.venv`, which is a local host environment and will not run inside Linux). If Positron does not list `/opt/venv/bin/python`, open **Preferences: Open Remote Settings (JSON)** and set `"python.defaultInterpreterPath": "/opt/venv/bin/python"`, then reload the window. Verify in the Console by running:
   ```python
   import sys
   print(sys.executable)
   ```
   This should print `/opt/venv/bin/python`.
8. When you are done working, close the remote Positron window and stop the container from a terminal on your computer:
   ```bash
   docker compose down
   ```

### Troubleshooting Container SSH Connections

- **`~/.ssh/id_ed25519.pub` or `~/.gitconfig` became a folder:** Docker creates a directory if a mounted file does not exist yet. Run `docker compose down`, delete the empty folder, create the key or run `git config --global`, and run `docker compose up -d` again.
- **"Remote host identification has changed":** This happens when the container image updates. Run `ssh-keygen -R "[localhost]:2222"` and reconnect.
- **Permission denied on Windows or Linux:** Ensure `StrictModes no` is enabled in `Dockerfile` (already enabled on our image) and that your key is at `~/.ssh/id_ed25519.pub`.
- **Port `2222` is already in use:** Stop any other running container using port `2222` (`docker ps`), or change the first `2222` in `docker-compose.yml` to another port (such as `2223`) and update `~/.ssh/config` to match.
- **Many unchanged files show as modified on Windows:** Run `git config --local core.autocrlf true` inside `/workspace` so Linux Git matches Windows line endings.

## Adding or Updating Packages

1. Create and switch to a new feature branch (never push directly to `main`).
2. Inside the container, add or update the package with `uv`, ensuring all versions in `pyproject.toml` are pinned with `==` (not `>=`) and `uv.lock` is updated.
3. Commit `pyproject.toml` and `uv.lock` together and push your branch.
4. Wait for the **Publish Docker Image** GitHub Actions workflow to finish building the multi-platform (`linux/amd64` and `linux/arm64`) image and committing the updated `sha-` tag to `docker-compose.yml` on your branch.
5. Run `git pull` and `docker compose pull` to verify the updated image, then open a Pull Request and have a teammate review it before merging.
6. After merging to `main`, wait for the workflow run on `main` to finish, then run `git pull` on `main` and `docker compose pull` so everyone uses the latest image.

## Republishing the Report on GitHub Pages

Our published report is served from `docs/index.html` using a self-contained HTML build (`embed-resources: true` in `analysis/council-voting-analysis.qmd`). Whenever you update and re-render the report inside the container, copy the new HTML file into `docs/` and push:

```bash
uv run quarto render analysis/council-voting-analysis.qmd
mkdir -p docs
cp analysis/council-voting-analysis.html docs/index.html
touch docs/.nojekyll
```

Commit both `analysis/council-voting-analysis.qmd` and `docs/index.html` (and keep `docs/.nojekyll` intact) before pushing.

## Reporting Issues and Submitting Pull Requests

Use GitHub Issues to report bugs, propose changes, and coordinate work with teammates. For every change, create a small, descriptively named branch in this repository (not a fork), write clear commit messages, and open a Pull Request against `main`. At least one human teammate must review and approve every Pull Request before it is merged.

## AI Policy

Contributors may use generative AI tools to assist with learning, debugging, and drafting documentation, provided all outputs are reviewed and verified by a human. AI tools or agents must never open, review, approve, or merge Pull Requests or GitHub Issues on behalf of team members. Any AI assistance used in the project must be disclosed transparently in [README.md](README.md).