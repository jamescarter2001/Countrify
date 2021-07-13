# Countrify

Command line tool for checking the region availability of a Spotify track.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python Countrify.py -i 'https://open.spotify.com/example' -r 'REGION_CODE'
```
You'll need to set a Client ID + Client Secret in `config.ini` by creating a new application on the 
Spotify Developer website.

## Credit

__[@shirtjs](https://twitter.com/shirtjs)__: argparse integration
