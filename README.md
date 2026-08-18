# contactsls

`contactsls` is a read-only command-line viewer for the local macOS Contacts databases. By default it prints the ten most recently created named contacts.

```sh
contactsls
contactsls --sort modified -n 25 --fields name,modified,emails
contactsls --match "Dale Barnes" --details --format json
contactsls --sort name --all --fields name,phones
contactsls --timeline ~/Downloads/location-history.json \
  --fields name,created,location
```

It opens the local SQLite databases in read-only mode. It does not automate Contacts.app, sign in to a service, or alter contact data. An optional Google Timeline JSON file is read locally to associate your approximate location when a contact was created. Reverse geocoding is opt-in and sends only the matched coordinates to Apple's geocoding service. Read the [usage guide](docs/usage.md) for every option and the Zsh completion setup.

## Install

### Homebrew

```sh
brew install marqueymarc/tap/contactsls
```

Homebrew installs the command and a compiled Apple Core Location reverse-geocoding helper. It is intended for macOS.

### From source

```sh
git clone https://github.com/marqueymarc/contactsls.git
cd contactsls
ln -s "$PWD/contactsls" ~/.local/bin/contactsls
mkdir -p ~/.zfunc
ln -s "$PWD/completions/_contactsls" ~/.zfunc/_contactsls
```

Make sure `~/.local/bin` is in `PATH`, and add `~/.zfunc` to Zsh's `fpath` before running `compinit`.

## Platform and privacy

The Contacts adapter is macOS-specific: it discovers the per-source Contacts Core Data SQLite stores under `~/Library/Application Support/AddressBook/Sources/` and opens them with SQLite `mode=ro`. Those internal schemas can change with macOS, so `contactsls` intentionally discovers the relevant entities and columns at runtime.

`--timeline` reads a Google Timeline export from disk; it does not upload the file. `--location` is the sole networked operation: it asks Apple to reverse-geocode the coordinates matched from that local export. The rest of the command, including normal contact listing, stays local and read-only. Source installations need the `swift` command for `--location`; the Homebrew formula compiles that helper during installation.

## Releases and visibility

The project is MIT licensed and has a public site at <https://marqueymarc.github.io/contactsls/>. Every future `vX.Y.Z` tag validates the command, creates GitHub release notes, and can update the Homebrew formula. The cross-repository update needs a `HOMEBREW_TAP_TOKEN` repository secret with write access to `marqueymarc/homebrew-tap`; without it, the tap's scheduled updater remains the fallback.

Release announcements are deliberately opt-in. Configure Mastodon, Bluesky, or a generic webhook (for services such as LinkedIn automation) using the [promotion guide](docs/promotion.md). The workflow otherwise does nothing—no social account is contacted by default.
