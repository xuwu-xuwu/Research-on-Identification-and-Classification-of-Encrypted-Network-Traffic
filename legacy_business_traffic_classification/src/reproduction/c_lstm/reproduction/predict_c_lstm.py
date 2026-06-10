#!/usr/bin/env python
from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "predict_c_lstm.py"
    runpy.run_path(str(target), run_name="__main__")
