# Node Version Manager [][3] [][4] [](https://bestpractices.dev/projects/684)

## Table of Contents

- [Intro](#intro)
- [About](#about)
- [Installing and Updating](#installing-and-updating)
 - [Install & Update Script](#install--update-script)
 - [Additional Notes](#additional-notes)
 - [Installing in Docker](#installing-in-docker)
 - [Installing in Docker for CICD-Jobs](#installing-in-docker-for-cicd-jobs)
 - [Troubleshooting on Linux](#troubleshooting-on-linux)
 - [Troubleshooting on macOS](#troubleshooting-on-macos)
 - [Ansible](#ansible)
 - [Verify Installation](#verify-installation)
 - [Important Notes](#important-notes)
 - [Git Install](#git-install)
 - [Manual Install](#manual-install)
 - [Manual Upgrade](#manual-upgrade)
- [Usage](#usage)
 - [Long-term Support](#long-term-support)
 - [Migrating Global Packages While Installing](#migrating-global-packages-while-installing)
 - [Migrating Global Packages Between Installed Versions](#migrating-global-packages-between-installed-versions)
 - [Offline Install](#offline-install)
 - [Default Global Packages From File While Installing](#default-global-packages-from-file-while-installing)
 - [io.js](#iojs)
 - [System Version of Node](#system-version-of-node)
 - [Listing Versions](#listing-versions)
 - [Setting Custom Colors](#setting-custom-colors)
 - [Persisting custom colors](#persisting-custom-colors)
 - [Suppressing colorized output](#suppressing-colorized-output)
 - [Restoring PATH](#restoring-path)
 - [Set default node version](#set-default-node-version)
 - [Use a mirror of node binaries](#use-a-mirror-of-node-binaries)
 - [Pass Authorization header to mirror](#pass-authorization-header-to-mirror)
 - [Platforms without official binaries](#platforms-without-official-binaries)
 - [.nvmrc](#nvmrc)
 - [Deeper Shell Integration](#deeper-shell-integration)
 - [Calling `nvm use` automatically in a directory with a `.nvmrc` file](#calling-nvm-use-automatically-in-a-directory-with-a-nvmrc-file)
 - [bash](#bash)
 - [zsh](#zsh)
 - [fish](#fish)
- [Running Tests](#running-tests)
- [Environment variables](#environment-variables)
- [Bash Completion](#bash-completion)
 - [Usage](#usage-1)
- [Compatibility Issues](#compatibility-issues)
- [Installing nvm on Alpine Linux](#installing-nvm-on-alpine-linux)
 - [Alpine Linux 3.13+](#alpine-linux-313)
 - [Alpine Linux 3.5 - 3.12](#alpine-linux-35---312)
- [Uninstalling / Removal](#uninstalling--removal)
 - [Manual Uninstall](#manual-uninstall)
- [Docker For Development Environment](#docker-for-development-environment)
- [Problems](#problems)
- [macOS Troubleshooting](#macos-troubleshooting)
- [WSL Troubleshooting](#wsl-troubleshooting)
- [Maintainers](#maintainers)
- [Project Support](#project-support)
- [Enterprise Support](#enterprise-support)
- [License](#license)
- [Copyright notice](#copyright-notice)

## Intro

`nvm` allows you to quickly install and use different versions of [node](https://nodejs.org) via the command line.

**Example:**
```sh
$ nvm install 24
Now using node v24.14.0 (npm v11.9.0)
$ node -v
v24.14.0
$ nvm use 22
Now using node v22.22.1 (npm v10.9.4)
$ node -v
v22.22.1
$ nvm use 20
Now using node v20.20.1 (npm v10.8.2)
$ node -v
v20.20.1
```

Simple as that!

## About
nvm is a version manager for [node.js](https://nodejs.org/en/), designed to be installed per-user, and invoked per-shell. `nvm` works on any POSIX-compliant shell (sh, [dash](https://git.kernel.org/pub/scm/utils/dash/dash.git), [ksh](https://github.com/ksh93/ksh), [zsh](https://www.zsh.org), [bash](https://www.gnu.org/software/bash/)), in particular on these platforms: unix, [macOS](https://www.apple.com/macos/), and [Windows WSL](https://github.com/nvm-sh/nvm#important-notes).

## Installing and Updating

### Install & Update Script

To **install** or **update** nvm, you should run the [install script][2]. To do that, you may either download and run the script manually, or use the following [cURL](https://curl.se) or [Wget](https://www.gnu.org/software/wget/) command:
```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
```
```sh
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
```

Running either of the above commands downloads a script and runs it. The script clones the nvm repository to `~/.nvm`, and attempts to add the source lines from the snippet below to the correct profile file (`~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, or `~/.profile`). If you find the install script is updating the wrong profile file, set the `$PROFILE` env var to the profile file’s path, and then rerun the installation script.

```sh
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

#### Additional Notes

- If the environment variable `$XDG_CONFIG_HOME` is present, it will place the `nvm` files there.

- You can add `--no-use` to the end of the above script to postpone using `nvm` until you manually [`use`](#usage) it:

```sh
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" --no-use # This loads nvm, without auto-using the default version
```

- You can customize the install source, directory, profile, and version using the `NVM_SOURCE`, `NVM_DIR`, `PROFILE`, and `NODE_VERSION` variables.
Eg: `curl ... | NVM_DIR="path/to/nvm"`. Ensure that the `NVM_DIR` does not contain a trailing slash.

- The installer can use [`git`](https://git-scm.com/), `curl`, or `wget` to download `nvm`, whichever is available.

- You can instruct the installer to not edit your shell config (for example if you already get completions via a [zsh nvm plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/nvm)) by setting `PROFILE=/dev/null` before running the `install.sh` script. Here's an example one-line command to do that: `PROFILE=/dev/null bash