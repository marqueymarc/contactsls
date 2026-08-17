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

## Estimated add location

Supply an exported Google Maps `location-history.json` file with `--timeline PATH`, or set `CONTACTSLS_TIMELINE` to its path. The file is read locally; the command makes no network requests. Location fields are intentionally estimates of where **you** were when the contact was created, not assertions about where you met.

```sh
contactsls --timeline ~/Downloads/location-history.json \
  --fields name,created,estimated_added_location,location_confidence

export CONTACTSLS_TIMELINE=~/Downloads/location-history.json
contactsls --fields name,estimated_added_location,location_time,location_delta
```

| Field or option | Meaning |
| --- | --- |
| `estimated_added_location` | Summary by default: best available name/address/city or coordinates, plus time delta. |
| `location_time`, `location_delta` | Timestamp of the matched Timeline event and its offset from contact creation. |
| `location_confidence`, `location_kind` | `high` for a covering visit; `medium` for a nearby visit/activity; `low` for a nearby raw point. |
| `location_coordinates`, `location_link` | Exact coordinates or a Google Maps link, available only on explicit request. |
| `--location summary\|place\|address\|city\|coordinates\|link` | Controls the `estimated_added_location` rendering. |
| `--location-window MINUTES` | Maximum offset for a nearby match; default 30 minutes. |

Run `contactsls --help` for the same information with examples.

## Installation and completion

The executable is symlinked at `~/.local/bin/contactsls`, and `~/.local/bin` is already on the shell PATH. Its Zsh completion is installed at `~/.zfunc/_contactsls`. It completes all flags, sort/format values, output fields, and Contacts database paths after `--db`.

Open a new Zsh terminal (or run `autoload -Uz compinit && compinit`) if the completion is not immediately available in an existing shell.
