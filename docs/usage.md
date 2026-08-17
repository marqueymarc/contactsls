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
| `--fields LIST` | Choose comma-separated output columns: `name`, `created`, `modified`, `organization`, `emails`, `phones`, `source`. |
| `--details` | Shorthand for every available column. |
| `--format table\|tsv\|json` | Select human-readable, tab-separated, or JSON output. |
| `--match TEXT` | Case-insensitive filter over name, organization, email, and phone data. |
| `--include-unnamed` | Include records with no visible name or organization. |
| `--db PATH` | Read one specified `AddressBook-v22.abcddb` database. It can be provided more than once. |

Run `contactsls --help` for the same information with examples.

## Installation and completion

The executable is symlinked at `~/.local/bin/contactsls`, and `~/.local/bin` is already on the shell PATH. Its Zsh completion is installed at `~/.zfunc/_contactsls`. It completes all flags, sort/format values, output fields, and Contacts database paths after `--db`.

Open a new Zsh terminal (or run `autoload -Uz compinit && compinit`) if the completion is not immediately available in an existing shell.
