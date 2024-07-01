To create a CI/CD pipeline for the Nexus deployment using GitHub Actions, you can define a workflow in a `.yml` file under the `.github/workflows` directory in your repository. Below is an example of how you can set up the GitHub Actions workflow based on the steps provided in the image:

```yaml
name: Deploy Nexus

on:
  push:
    branches:
      - sit

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'  # Adjust the Python version as needed

      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt

      - name: Pull latest changes from git
        run: |
          git reset --hard
          git pull origin sit

      - name: Enable Python virtual environment
        run: |
          source files/virtual_envs/.NexusEnv/bin/activate

      - name: Collect static files
        run: |
          source files/virtual_envs/.NexusEnv/bin/activate
          python manage.py collectstatic --noinput

      - name: Restart Gunicorn service
        run: |
          sudo systemctl restart gunicorn-sit_nexus.service

      - name: Reload Nginx
        run: |
          sudo nginx -s reload
```

### Explanation:

1. **Trigger**:
   - The workflow triggers on any push to the `sit` branch.

2. **Jobs**:
   - The `deploy` job runs on the latest Ubuntu runner.

3. **Steps**:
   - **Checkout code**: Uses the `actions/checkout` action to clone the repository.
   - **Set up Python**: Sets up the specified Python version.
   - **Install dependencies**: Creates a virtual environment and installs the dependencies.
   - **Pull latest changes**: Resets any local changes and pulls the latest code from the `sit` branch.
   - **Enable Python virtual environment**: Activates the specific Python virtual environment.
   - **Collect static files**: Collects static files using Django's `collectstatic` command.
   - **Restart Gunicorn service**: Restarts the Gunicorn service.
   - **Reload Nginx**: Reloads the Nginx service to apply any new configurations.

Make sure you have your project dependencies listed in a `requirements.txt` file in your repository. This file is used in the `Install dependencies` step to set up the environment correctly.

### Notes:
- This example assumes you have the necessary sudo permissions set up for the GitHub runner to restart services. If your services require elevated permissions, you might need to configure `sudo` without a password for the GitHub Actions runner user, or you might need to use SSH to connect to a remote server and perform these actions.

Save this YAML file as `.github/workflows/deploy.yml` in your repository to automate the deployment process.
