# Build a release manually

Please follow these steps to produce a release

## Checkout correct branch

Checkout the branch for which the release is to be build. If no branch exists for the new release one must be created. The name must correspond to the Netbox version in the format "netbox/MAJOR.MINOR".

## Set version number

For patch releases the version number in `pyproject.toml` and the `NetBoxInitializersConfig` needs to be updated. If the release is for a new Netbox version additional changes need to be made in `README.md` and `Dockerfile` (for tests).

## Build the packages

Install the needed Python packages for the build:

```bash
pip install --upgrade poetry
```

Then run the build for the wheel and source distributions:

```bash
poetry build
```

## Upload packages to PyPi

```bash
poetry publish
```
