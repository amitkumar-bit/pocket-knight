<p align="center">
  <img src="assets/pocket-knight.png" alt="A cat-shaped chess knight on an indigo chessboard" width="900">
</p>

# Pocket Knight

**A 4,092-byte chess engine in pure Python.** Pocket Knight plays legal chess with deterministic search using Python 3.13 and the standard library. It was built for the make.fun 4 KiB chess-engine bounty. [Competition rules](https://make.fun/bounty/tiny-chess-01)

[Try the demo](#try-it) · [Read the source](engine.py) · [Competition snapshot](https://github.com/amitkumar-bit/pocket-knight/tree/makefun-entry)

## Try it

Clone the repository and run the mate-in-one demo with Python 3.13. It prints a legal mating move in UCI notation.

```sh
git clone https://github.com/amitkumar-bit/pocket-knight.git
cd pocket-knight
python examples/mate_in_one.py
```

## Official practice result

| Elo | Wins | Spare plies |
| ---: | ---: | ---: |
| 2,112 | 6/6 | 719 |

These scores come from make.fun’s practice grader for the 4,092-byte submission. [Official Pocket Knight result](https://make.fun/api/submissions/01a208e6-7874-7019-9d38-8a6f800a35ff)

## Inside the engine

- A 0x88 board supports legal move generation, including castling, en passant, and all four promotions.
- Iterative-deepening negamax uses principal-variation search, a transposition table, and quiescence search.
- Incremental tapered evaluation scores material, piece placement, king cover, and pawn structure.
- Fixed node budgets make move selection reproducible.

## Rebuild the competition entry

`engine.py` is the readable source for the packed `main.py`. The `makefun-entry` tag pins the exact submitted commit. With the competition kit downloaded, run its compressor from the repository root.

```sh
node path/to/tiny-chess-01-kit/cli/makefun.mjs compress engine.py --out rebuilt.py
```

The competition entrypoint plays through make.fun’s HTTP referee at `MAKEFUN_ENV_URL`. The local demo calls the same engine directly. [Python entrypoint](main.py) · [MIT license](LICENSE)

If Pocket Knight gives you an idea for your own tiny engine, a star helps other chess programmers find it.
