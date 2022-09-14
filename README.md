### Hexlet tests and linter status:

[![Actions Status](https://github.com/asidowner/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/asidowner/python-project-lvl3/actions)

### Project tests status:

[![page-loader-check](https://github.com/asidowner/python-project-lvl3/actions/workflows/page-loader-check.yml/badge.svg)](https://github.com/asidowner/python-project-lvl3/actions/workflows/page-loader-check.yml)

### Maintainability

[![Maintainability](https://api.codeclimate.com/v1/badges/fcfcec0a358189655fa8/maintainability)](https://codeclimate.com/github/asidowner/python-project-lvl3/maintainability)

### Test Coverage

[![Test Coverage](https://api.codeclimate.com/v1/badges/fcfcec0a358189655fa8/test_coverage)](https://codeclimate.com/github/asidowner/python-project-lvl3/test_coverage)

### Installation

Make sure you are running at least Python 3.7

```commandline
git clone https://github.com/asidowner/python-project-lvl3
cd python-project-lvl3 && make install && make build && make package-install
```

### Example

```commandline
page-loader --output /var/tmp https://google.com/
echo "path to file"
/var/tmp/google-com.html
```

### Logging

If you want change logging level you can set this on environment params - `PAGE_LOADER_LOGGING_LEVEL`.
By default, logging level set as `INFO`.

Available value:
* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL
* NOTSET

### Help

```commandline
page-loader -h
```

### Example

[![asciicast](https://asciinema.org/a/JoyAFaUbimoNdnjaFSqBRcOqt.svg)](https://asciinema.org/a/JoyAFaUbimoNdnjaFSqBRcOqt)

### Example load site with page

[![asciicast](https://asciinema.org/a/dYyyTlCKhOweP13L3ieafyXTl.svg)](https://asciinema.org/a/dYyyTlCKhOweP13L3ieafyXTl)

### Example with logging

[![asciicast](https://asciinema.org/a/5XSBUzu4TvbWOeX3d3fShSQtm.svg)](https://asciinema.org/a/5XSBUzu4TvbWOeX3d3fShSQtm)

### Example with progress bar
[![asciicast](https://asciinema.org/a/LepnLmvnf4ocdG9NLESR9GWso.svg)](https://asciinema.org/a/LepnLmvnf4ocdG9NLESR9GWso)