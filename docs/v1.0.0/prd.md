# PRD: Fintrack v1.0.0

## Problem Statement

For command-line enthusiasts and developers, switching to a browser or mobile app to log quick daily transactions creates unnecessary context switching and friction. Existing CLI tools are either overly complex or lack simple local storage. Fintrack provides a lightweight, keyboard-driven CLI finance tracker that enables instantaneous local logging and balance tracking directly from the shell.

## Target User

Developers, sysadmins, and power users who spend primary working hours in a Unix-like terminal environment and value speed, offline capability, and scriptability over rich graphical interfaces.

## Goals

- **Blazing Fast Logging:** Enable logging an expense or income transaction in < 3 seconds via a single shell command.
- **Instant Visibility:** View total balance and category breakdowns directly from stdout.
- **Zero-Config Persistence:** Store data locally out of the box (SQLite) without requiring external server setup or authentication.

## Non-Goals (Out of Scope for v1.0.0)

- Remote cloud/Google Sheets synchronization (deferred to v2.0 due to OAuth overhead).
- Multi-currency support or multi-account tracking.
- CSV/JSON export/import commands.
- Interactive TUI (Terminal User Interface using ncurses/Textual) — v1 focus is strict CLI arguments.

## Core Features (MVP)

### 1. Transaction Management (CLI)

- **Add Transaction:** Single command execution with flags for amount, type (income/expense), category, and optional note.
  - _Syntax:_ `fintrack log --type expense --amount 12.50 --category food --note "Lunch"`
- **List Transactions:** View recent transactions in a formatted ASCII/Markdown table in the terminal.
  - _Syntax:_ `fintrack list --limit 10`
- **Delete Transaction:** Remove a entry by ID (`fintrack delete <id>`).

### 2. Account Balance & Summary

- **Current Balance:** Command to output total net balance (`fintrack balance`).
- **Category Breakdown:** Basic summary of spending grouped by category (`fintrack summary`).

### 3. Category Configuration

- Default categories pre-loaded (`Food`, `Transport`, `Utilities`, `Income`).
- User can add custom categories via CLI (`fintrack category add <name>`).

## Technical Constraints & Execution Strategy

- **Timeline:** Aug 03, 2026 – Aug 30, 2026 (~12 hours total dev time).
- **Tech Stack:** Python 3.13+ using `Click` (for CLI handling), `Rich` (for terminal formatting), and built-in `sqlite3`.
- **Distribution:** Standalone Python package runnable via `pipx` or shell alias.

## Success Metrics

- **Speed:** User can log a standard expense from any shell prompt in under 3 seconds.
- **Reliability:** 100% local persistence rate (zero data loss on invalid inputs/malformed flags).
- **Simplicity:** Entire v1 codebase remains under 500 lines of Python code for easy personal maintenance.
