# The Passport of the Republic of Vesskara

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-7c3aed)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)

Entry for the make.fun bounty [The Passport Page of a Country That Isn't There](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318).

`main.py` (Python 3.13, standard library only, no network) draws and writes
one image to `/output/entry.png`: an open passport spread of the Republic of
Vesskara, an island country that does not exist.

The left page is the data page: a portrait with a faded ghost copy, the
holder's personal details (Mara Elisabeth Voss of Port Lumen), a signature,
and a two-line machine-readable zone. The right page carries visas and border
stamps from the neighbouring countries Kordavia, Thalassia and the Meridian
Union — plus a glued-in Tide Permit, the one piece of paperwork that reveals
the place: the ferry to Port Lumen sails only at high tide, the channel is
dry at low water, no road leaves the island, and the passport is valid for
travel by sea only.

The image is 1024 x 720 PNG, well under the 1 MiB gate.

## Run

```sh
python3 main.py   # writes /output/entry.png
```
