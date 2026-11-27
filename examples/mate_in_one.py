"""Run the packed Pocket Knight engine on a mate-in-one position."""

from pathlib import Path
from runpy import run_path


if __name__ == "__main__":
    entrypoint = Path(__file__).resolve().parents[1] / "main.py"
    engine = run_path(str(entrypoint))
    fen = "7k/5Q2/6K1/8/8/8/8/8 w - - 0 1"
    position = engine["Position"](fen)
    moves = [engine["uci"](move) for move in position.legal()]
    print(engine["choose"](fen, moves, nodes=5_000))
