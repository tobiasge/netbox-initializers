# Prepare a release

Please follow these steps to produce a release

## Checkout correct branch

Checkout the branch for which the release is to be build. If no branch exists for the new release one must be created. The name must correspond to the Netbox version in the format "netbox/MAJOR.MINOR".

## Set version number

For patch releases the version number in `pyproject.toml` and the `NetBoxInitializersConfig` needs to be updated. If the release is for a new Netbox version additional changes need to be made in `README.md` and `Dockerfile` (for tests).

## Build the release automatically

After changing the version numbers and committing them create a new release with the GitHub Web UI. Configure the release to create a new tag with the name `vX.Y.Z`.

## Build the release manually

### Build the packages

Install the needed Python packages for the build:

```bash
pip install --upgrade poetry
```

Then run the build for the wheel and source distributions:

```bash
poetry build
```

### Upload packages to PyPi

```bash
poetry publish
```
