# PyPassGen
A command line tool for generating passwords using the secrets and string modules

## Features
- Clean and cryptographically secure password generation through the secrets module
- Flexible customization of output, can set a combination of numbers, uppercase, lowercase, and symbols to customize the output
- Can generate multiple passwords at once using the --count flag
- Allows clipboard (through wl-copy)
- Displays entropy bits

## Installation
```
bash
git clone https://github.com/Lyzanov/PyPassGen
cd PyPassGen
```

## Usage

```
bash
pypassgen -iups --copy
```

## Tech Stack
- Python
- Secrets: Generate secure random numbers for managing secrets
- Argparse: Parser for command-line options, arguments and subcommands

## Author's Note:
This is not meant to replace conventional password managers/generators like bitwarden. This was developed as a learning project and an addition to my portfolio

## License:
MIT
