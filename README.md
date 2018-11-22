# Restatic - A Boring Open Source GUI for Restic
[![Build Status](https://travis-ci.org/Mebus/restatic.svg?branch=master)](https://travis-ci.org/Mebus/restatic)

:warning: :warning: ***This is still under heavy developement and currently unusable !!! It's a fork of [Vorta](https://github.com/borgbase/vorta).*** :warning: :warning:

Restatic is an open source Linux / Windows GUI for [Restic](https://restic.net). It's currently in very early alpha status. 

## Main features

- Encrypted, deduplicated and compressed backups.
- Works with any local or remote Borg repo. 
- Add SSH keys and initialize repos directly from the GUI.
- Repo keys are securely stored in KWallet.
- Mount existing archives via FUSE.
- Manage multiple backup profiles with different source folders, destinations and settings.
- Prune and check backups periodically.
- Flexible scheduling for automatic background backups.
- View a list of archives and action logs.
- Exclude options/patterns.

## Installation and Download
Restatic should work on all platforms that support Qt and Borg. 

### Linux / Windows
First install Borg and its [dependencies](https://restic.net/). Then install Restatic from Pypi:
```
$ pip install restatic
```

After installation run with the `restatic` command.
```
$ restatic
```

## Debugging and Bugs
Please report any errors you may encounter by [opening an issue](https://github.com/Mebus/restatic/issues) on Github. Please include steps to reproduce and all logging output. Logs can be found in these folders:

- Linux: `$HOME/.cache/Restatic/log`
- macOS: `$HOME/Library/Logs/Restatic`

## Development

Install in development/editable mode while in the repo:
```
$ pip install -e .
```

Then run as Python script:
```
$ restatic
```

Install developer packages we use (pytest, tox, pyinstaller):
```
pip install -r requirements-dev.txt
```

Qt Creator is used to edit views. Install from [their site](https://www.qt.io/download) or using Homebrew and then open the .ui files in `restatic/UI`:
```
$ brew cask install qt-creator
$ brew install qt
```

### Testing (work in progress)

Tests are in the folder `/tests`. Testing happens at the level of UI components. Calls to `restic` are mocked and can be replaced with some example json-output. To run tests:
```
$ pytest
```

## Privacy Policy
- No personal data is ever stored or transmitted by this application.
- During beta, crash reports are sent to [Sentry](https://sentry.io) to quickly find bugs. You can disable this by setting the env variable `NO_SENTRY=1`. Your repo password will be scrubbed *before* the test report is transmitted.

## Authors
 - (C) 2018 Manuel Riel for [BorgBase.com](https://www.borgbase.com)
 - (C) 2018 Mebus, https://github.com/Mebus/

## License and Credits
- Licensed under GPLv3. See LICENSE.txt for details.
- Uses the excellent [Restic](https://restic.net/)
- Based on [PyQt](https://riverbankcomputing.com/software/pyqt/intro) and [Qt](https://www.qt.io).
- Icons by [FontAwesome](https://fontawesome.com)
