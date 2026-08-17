# contactsls

`contactsls` is a read-only command-line viewer for the local macOS Contacts databases. By default it prints the ten most recently created named contacts.

```sh
contactsls
contactsls --sort modified -n 25 --fields name,modified,emails
contactsls --match "Dale Barnes" --details --format json
contactsls --sort name --all --fields name,phones
```

It opens the local SQLite databases in read-only mode. It does not automate Contacts.app, sign in to a service, alter contact data, or use a network connection. Read the [usage guide](docs/usage.md) for every option and the Zsh completion setup.

## Install

```sh
git clone https://github.com/marqueymarc/contactsls.git
cd contactsls
ln -s "$PWD/contactsls" ~/.local/bin/contactsls
mkdir -p ~/.zfunc
ln -s "$PWD/completions/_contactsls" ~/.zfunc/_contactsls
```

Make sure `~/.local/bin` is in `PATH`, and add `~/.zfunc` to Zsh's `fpath` before running `compinit`.
