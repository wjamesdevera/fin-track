# Fin-Track — Command Reference

> **Version:** 1.0.0  
> **Last Updated:** 2026-05-30  
> **Maintainer:** wjamesdevera  
> **Repository / Homepage:** https://github.com/wjamesdevera/fin-track

---

## Table of Contents

1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Global Options](#global-options)
4. [Commands](#commands)
   - [command-one](#command-one)
   - [command-two](#command-two)
   - [command-three](#command-three)
5. [Configuration](#configuration)
6. [Environment Variables](#environment-variables)
7. [Exit Codes](#exit-codes)
8. [Examples & Recipes](#examples--recipes)
9. [Troubleshooting](#troubleshooting)
10. [Changelog](#changelog)

---

## Overview

FinTrack is a lightweight Command Line Interface (CLI) financial management tool designed for rapid expense and income logging. By leveraging a terminal-based environment, FinTrack provides a high-velocity alternative to bulky mobile apps or manual spreadsheets. This project aims to eliminate the "logging friction" that prevents consistent financial tracking for power users who spend their time in a development environment.

```
ftrack [global-options] <command> [command-options] [arguments]
```

---

## Installation & Setup

<!-- TODO: Add installation and setup -->

Coming Soon

**Requirements:**

- OS: Windows / macOS / Linux
- Runtime: go version go1.24.5 linux/amd64
<!-- TODO: Add permission in docs -->
- Permissions: [any special permissions needed]

---

## Global Options

These flags apply to every command.

| Flag        | Alias | Type    | Default     | Description                                   |
| ----------- | ----- | ------- | ----------- | --------------------------------------------- |
| `--help`    | `-h`  | boolean | —           | Show help text and exit                       |
| `--version` | `-v`  | boolean | —           | Print version number and exit                 |
| `--verbose` | —     | boolean | `false`     | Enable detailed output                        |
| `--quiet`   | `-q`  | boolean | `false`     | Suppress all output except errors             |
| `--config`  | `-c`  | string  | `~/.toolrc` | Path to config file                           |
| `--output`  | `-o`  | string  | `stdout`    | Output destination (`stdout`, `file`, `json`) |

---

## Commands

---

<!-- ### `command-one`

**Short description:** One sentence on what this command does.

```
tool-name command-one [options] <required-arg> [optional-arg]
```

#### Arguments

| Argument       | Required | Description                                             |
| -------------- | -------- | ------------------------------------------------------- |
| `required-arg` | ✅       | What this argument represents                           |
| `optional-arg` | ❌       | What this argument represents, and its default behavior |

#### Options

| Flag           | Alias | Type    | Default   | Description                   |
| -------------- | ----- | ------- | --------- | ----------------------------- |
| `--flag-one`   | `-f`  | string  | `default` | What this flag controls       |
| `--flag-two`   | —     | boolean | `false`   | What this flag enables        |
| `--flag-three` | `-t`  | number  | `10`      | Numeric parameter description |

#### Examples

```bash
# Basic usage
tool-name command-one my-argument

# With options
tool-name command-one --flag-one value my-argument

# Piping output
tool-name command-one my-argument | grep "pattern"
```

#### Notes / Caveats

- Any behavioral quirks, edge cases, or important warnings go here.
- e.g., "This command modifies files in place — always back up first." -->

<!-- ---

### `command-two`

**Short description:** One sentence on what this command does.

```
tool-name command-two [options] <target>
```

#### Arguments

| Argument | Required | Description                                    |
| -------- | -------- | ---------------------------------------------- |
| `target` | ✅       | The target resource (file path, URL, ID, etc.) |

#### Options

| Flag        | Alias | Type    | Default | Description                           |
| ----------- | ----- | ------- | ------- | ------------------------------------- |
| `--dry-run` | `-n`  | boolean | `false` | Preview changes without applying them |
| `--force`   | —     | boolean | `false` | Skip confirmation prompts             |

#### Examples

```bash
# Dry run first (recommended)
tool-name command-two --dry-run ./target-path

# Apply for real
tool-name command-two ./target-path
```

#### Notes / Caveats

- Add any relevant warnings here.

--- -->

<!-- ### `command-three`

**Short description:** One sentence on what this command does.

```
tool-name command-three [options]
```

#### Options

| Flag       | Alias | Type   | Default | Description                           |
| ---------- | ----- | ------ | ------- | ------------------------------------- |
| `--format` | —     | string | `table` | Output format: `table`, `json`, `csv` |
| `--limit`  | `-l`  | number | `20`    | Maximum number of results to return   |

#### Examples -->

```bash
# Default output
tool-name command-three

# JSON output, limited to 5 results
tool-name command-three --format json --limit 5
```

<!-- ---

## Configuration

The tool looks for configuration in the following order (later sources override earlier ones):

1. Built-in defaults
2. `~/.toolrc` (global config file)
3. `.toolrc` in the current directory (project-level)
4. Environment variables (see below)
5. CLI flags passed at runtime

**Example config file (`.toolrc`):**

```yaml
# .toolrc
output: json
verbose: false
default_limit: 50

command-one:
  flag-one: custom-default
```

---

## Environment Variables

| Variable         | Description                                         | Default      |
| ---------------- | --------------------------------------------------- | ------------ |
| `TOOL_API_KEY`   | API key for authentication                          | _(none)_     |
| `TOOL_CONFIG`    | Override path to config file                        | `~/.toolrc`  |
| `TOOL_ENV`       | Runtime environment: `production`, `staging`, `dev` | `production` |
| `TOOL_LOG_LEVEL` | Log verbosity: `error`, `warn`, `info`, `debug`     | `warn`       |

---

## Exit Codes

| Code | Meaning                       |
| ---- | ----------------------------- |
| `0`  | Success                       |
| `1`  | General error                 |
| `2`  | Invalid usage / bad arguments |
| `3`  | Authentication failure        |
| `4`  | Resource not found            |
| `5`  | Network / timeout error       |

---

## Examples & Recipes

### Common Workflow A — [Describe task]

```bash
# Step 1: Do the first thing
tool-name command-one my-target

# Step 2: Verify
tool-name command-two --dry-run my-target

# Step 3: Apply
tool-name command-two my-target
```

### Common Workflow B — [Describe task]

```bash
# Get JSON output and pipe to jq
tool-name command-three --format json | jq '.items[] | select(.status == "active")'
```

---

## Troubleshooting

### Error: `Authentication failed`

**Cause:** Missing or invalid API key.
**Fix:** Set the `TOOL_API_KEY` environment variable or run `tool-name login`.

---

### Error: `Command not found`

**Cause:** Tool is not on your `PATH`.
**Fix:** Re-run the installation steps and confirm your shell's PATH includes the install directory.

---

### Command runs but produces no output

**Cause:** The `--quiet` flag may be set in your config file.
**Fix:** Run with `--verbose` to see detailed logs: `tool-name command-one --verbose my-arg`

--- -->

## Changelog

| Version | Date       | Summary         |
| ------- | ---------- | --------------- |
| 1.0.0   | YYYY-MM-DD | Initial release |
