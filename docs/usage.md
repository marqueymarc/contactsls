# contactsls

`contactsls` is a read-only command-line viewer for the Contacts databases on this Mac. It reads the local source databases directly in SQLite read-only mode; it does not automate Contacts.app, sign in anywhere, or modify a contact.

The default output is the ten newest named contacts, sorted by creation date with the newest first.

```sh
contactsls
```

## Common use

```sh
# Newest 25 by most-recent edit, including email addresses.
contactsls --sort modified --limit 25 --fields name,modified,emails

# All named contacts in alphabetical order with phone numbers.
contactsls --sort name --all --fields name,phones

# Find contacts using any name, organization, email address, or phone number.
contactsls --match "Dale Barnes" --details --format json

# Show oldest contacts first.
contactsls --sort created --oldest
```

## Options

| Option | Meaning |
| --- | --- |
| `--sort created\|modified\|name\|organization` | Select the sort criterion. Creation and modification dates are newest first by default; text sorts ascending. |
| `-n`, `--limit N` | Print at most `N` contacts. The default is 10. |
| `--all` | Print every matching contact, ignoring `--limit`. |
| `--oldest` | Reverse the selected order. |
| `--fields LIST` | Choose comma-separated output columns: `name`, `created`, `modified`, `organization`, `emails`, `phones`, `notes`, `source`, or a location field below. |
| `--details` | Shorthand for all contact fields, including `notes`. |
| `--format table\|tsv\|json` | Select human-readable, tab-separated, or JSON output. |
| `--match TEXT` | Case-insensitive filter over name, organization, email, and phone data. |
| `--include-unnamed` | Include records with no visible name or organization. |
| `--db PATH` | Read one specified `AddressBook-v22.abcddb` database. It can be provided more than once. |

## Contact-creation location

Supply an exported Google Maps `location-history.json` file with `--timeline PATH`, or set `CONTACTSLS_TIMELINE` to its path. The file is read locally. Location fields describe where **you** were when the contact was created, not assertions about where you met.

The importer supports both the current iPhone top-level segment-array export and older exports wrapped in `semanticSegments`. By default, `location` prints the matched coordinates. Add `--location` to reverse-geocode them into a readable place or address.

```sh
contactsls --timeline ~/Downloads/location-history.json \
  --fields name,created,location,location_confidence

export CONTACTSLS_TIMELINE=~/Downloads/location-history.json
contactsls --fields name,location,location_time,location_delta
```

| Field or option | Meaning |
| --- | --- |
| `location` | Coordinates by default; a readable place/address when one is present in the Timeline data. |
| `location_time`, `location_delta` | Start of the matched Timeline event and its offset from contact creation; a covering event reports `during visit` or `during activity`. |
| `location_confidence`, `location_kind` | `high` for a covering visit; `medium` for activity or nearby visit; `low` for a nearby raw point. |
| `location_coordinates`, `location_link` | Exact coordinates or a Google Maps link, available only on explicit request. |
| `--location` | Reverse-geocode matched coordinates with Apple Maps. This sends those coordinates to Apple; without it, `location` stays local coordinates only. |
| `--location-window MINUTES` | Maximum offset for a nearby match; default 30 minutes. |

Run `contactsls --help` for the same information with examples.

## macOS-specific behavior

`contactsls` reads the Contacts Core Data SQLite stores that macOS keeps under `~/Library/Application Support/AddressBook/Sources/`. This is an internal macOS data format, not a public Apple API; the command discovers the available schema at runtime and opens each database using SQLite read-only mode.

The optional `--location` switch runs the bundled Swift/Core Location helper. It sends the matched coordinates to Apple's reverse-geocoding service and therefore may require network access. Without that flag, the command does not make network requests: Contacts data and the Google Timeline export remain local. A source installation needs the `swift` command for this option; the Homebrew formula compiles the helper during installation.

## Homebrew installation

```sh
brew install marqueymarc/tap/contactsls
```

The formula packages the command and its helper, but not Contacts data or Timeline exports. Use the source installation above if you want a checkout you can edit directly.

## Installation and completion

The executable is symlinked at `~/.local/bin/contactsls`, and `~/.local/bin` is already on the shell PATH. Its Zsh completion is installed at `~/.zfunc/_contactsls`. It completes all flags, sort/format values, output fields, and Contacts database paths after `--db`.

Open a new Zsh terminal (or run `autoload -Uz compinit && compinit`) if the completion is not immediately available in an existing shell.
