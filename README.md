# LibCal Bookings

A simple description


## Instructions for working on this project


### Project development environment setup

#### First steps

Follow these steps to set up your development environment:

- Make sure the [production Docker environment](https://gitlab.com/byuhbll/docker-environment) is running. (Clone that repo, cd into it, and type `docker compose up -d`.)
- Clone the project repository by running `git clone git@gitlab.com:byuhbll/apps/libcal-bookings.git`.
- `cd` into `libcal-bookings`.

#### Option: Visual Studio Code Dev Containers
1. You will need to [install the Dev Containers extension](https://code.visualstudio.com/docs/devcontainers/tutorial#_install-the-extension), if you don't have it already.
2. Open the project in VS Code (`code .`). Since we have a `.devcontainer.json` file in the project, VS Code should prompt you to "Reopen in Container". Click this button and VS Code will attempt to build the container. If you don't get this prompt, you can open the Command Palette (`Ctrl`/`Cmd`+`Shift`+`P`), and run `Dev Containers: Reopen in Container`.
3. If successful, you will now be in the container. If you open your terminal in VS Code you should be in the `code` directory, and you can `ls` to see the top level files and folders.
4. In the terminal run `inv manage createsuperuser`. This creates a superuser. If it says the superuser already exists, then abort and continue with the next step. You should use your netId and the password shoudn't matter.
5. From the bash prompt in the application's container, run `inv run`. This starts the development server which you can access at http://localhost:8080/admin.
6. If you want to debug your code while in the container, run `cp .vscode/launch.example.json .vscode/launch.json`. This gives you a couple of default debug configurations that you can run with the [debugger](https://code.visualstudio.com/Docs/editor/debugging). You can also add more configurations as needed in the `launch.json` file (e.g. to test management commands). Set breakpoints, select the configuration, and run with the debugger.

To shut down the container from VS Code, open the Command Palette (`Ctrl`/`Cmd`+`Shift`+`P`), and run `Dev Containers: Reopen Folder Locally` (or `Dev Containers: Close Remote Connection`).

#### Option: Build and Run From Command Line
1. Run `docker compose up -d`, which will start the docker container for the application.
2. Run `docker compose exec app bash`, which will start a bash terminal running in the applications docker container.
3. From the bash prompt in the application's container, run `inv manage createsuperuser`. This creates a superuser. If it says the superuser already exists, then abort and continue with the next step. You should use your netId and the password shoudn't matter.
4. From the bash prompt in the application's container, run `inv run`. This starts the development server which you can access at http://localhost:8080/admin.
5. You can edit your code as usual (outside the container, using your normal editor).

Here are some examples of commands that you can run:

- `docker compose exec app bash` - starts a bash prompt inside the
application's docker container.
- `docker compose exec app inv migrate` - runs migrations inside the
application's docker container.
- `docker compose exec app inv manage [command]` - run a management command inside the container.

You can also run management commands and invoke commands in the container at the bash prompt.

To shut down the container:

- `docker compose down`

#### Common Gotchas
- If you are trying to build a container and you already have another container running (in the `docker-environment` network), using port `8080`, then you will either need to stop the running container, or if you want to have both running at the same time, create an `.env` file at the root of the project with contents `HOST_PORT=8081` (it doesn't have to be `8081`, but just a different port that is currently unused). Then rebuild the container and things should now work, and you will access the app through the port you set in the `.env` file.
- If you try and build the container and it says the network doesn't exist, make sure your `docker-environment` is up and running, then try rebuilding without the cache (VS Code: `Dev Containers: Rebuild Without Cache and Reopen in Container`).
- In VS Code, if you encounter issues using `git` to push/pull from GitLab from inside the Dev Container, you can have your GitLab credentials forwarded to the container via an ssh agent. See [Sharing Git credentials with your container](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials).

### Testing in this project

Run the project's tests with `docker compose exec app tox` from your terminal or simply `tox` from inside the container.

#### Testing in GitLab CI

Everything should work automatically thanks to `.gitlab-ci.yml`. You can edit `application-ci.yml` to tweak settings for the CI.

### Configuring this project

We use [Configuro](https://gitlab.com/byuhbll/lib/python/configuro) to load in configuration from YAML files and to override configuration items with environment variables. 

#### Development

In development you will use `application.yml` for configuration values which should not be added to `application-base.yml`. `application.yml` is not added to the git repo.

#### Test

When testing locally with `tox`, `application-test.yml` is used for the config file. When testing in a GitLab CI/CD pipeline, we use `application-ci.yml`.

#### Deploy

Our Kubernetes deploys will pull in configuration from `application-base.yml`, but will then use GitLab CI/CD variables to override configuration. Variables common to all of our projects are set at our [top-level namespace](https://gitlab.com/groups/byuhbll/-/settings/ci_cd) in GitLab. Variables specific to your project will be set at the [project level](https://gitlab.com/byuhbll/apps/libcal-bookings/-/settings/ci_cd). When setting a variable you can select which environment it should apply to (`production`, `staging`, `review/*`, or `All`).

To override a config item with an environment variable, the config item must be present in the `application-base.yml` file. So, make sure there is a default value or a placeholder in that file. For more information on overriding with environment variables [consult Configuro's documentation](https://gitlab.com/byuhbll/lib/python/configuro/-/blob/master/docs/user-guide.md).

### Deploying this project

Deployment to a Kubernetes cluster happens automatically through GitLab pipelines. Upon pushing a new brach to the GitLab repo, the pipeline will deploy an instance of the branch to our `review` environment. The `review` job will output the base URL that the application has deployed to, which will be of the form `some-subdomain-with-branch-name.review.lib.byu.edu`. For the review, staging, and production URL, you will need to add your base path (i.e. `/libcal-bookings`) to access the application. For example, the default admin URLs will be at:

- Review: https://{some-subdomain-with-branch-name}.review.lib.byu.edu/libcal-bookings/admin
    - If you only have one review branch, https://review.lib.byu.edu/libcal-bookings/admin
- Staging: https://staging.lib.byu.edu/libcal-bookings/admin
- Production: https://apps.lib.byu.edu/libcal-bookings/admin

The application will be deployed to our `staging` environment upon being merged into master. It will be deployed to `production` when it is tagged. Use [Semantic Versioning](https://semver.org/) to determine the tag number.
### Frontend build process

See the [frontend build process README](https://gitlab.com/byuhbll/lib/python/django-project-template/-/blob/master/frontend.md).
