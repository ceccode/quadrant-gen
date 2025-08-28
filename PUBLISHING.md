# Publishing Guide for Quadrant Generator

This document contains instructions for maintainers on how to publish new versions of the `quadrant-gen` package to PyPI.

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/ if you don't have one
2. Install required tools:
   ```bash
   pip install --upgrade pip setuptools wheel twine build
   ```

## Publishing Process

### 1. Update Version Numbers

Before publishing a new release, update the version number in:
- `setup.py`
- `quadrant_gen/__init__.py`

Follow [Semantic Versioning](https://semver.org/) principles:
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

### 2. Update Documentation

Ensure the README.md and other documentation reflect any changes in the new version.

### 3. Clean Previous Builds

Remove any previous build artifacts:

```bash
rm -rf build/ dist/ *.egg-info/
```

### 4. Build Distribution Packages

Build source distribution and wheel packages:

```bash
python setup.py sdist bdist_wheel
```

### 5. Check the Packages

Verify that the packages are valid:

```bash
twine check dist/*
```

### 6. Upload to PyPI

Upload the packages to PyPI:

```bash
twine upload dist/*
```

You'll be prompted for your PyPI username and password. After successful upload, your package will be available at:
`https://pypi.org/project/quadrant-gen/`

### 7. Verify Installation

Test that the package can be installed from PyPI:

```bash
pip install --upgrade quadrant-gen
```


## Creating a GitHub Release (Optional)

If you're using GitHub:

1. Tag the release:
   ```bash
   git tag -a v0.2.0 -m "Version 0.2.0"
   git push origin v0.2.0
   ```

2. Create a release on GitHub with release notes

## Automating with GitHub Actions (Future Enhancement)

TODO: setting up GitHub Actions to automatically build and publish the package when a new release is tagged.
