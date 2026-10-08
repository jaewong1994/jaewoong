# -*- coding: utf-8 -*-
"""W38 GEOa (cycle48) 독립 검산 — verify_W38_misc_cycle48.py 를 그대로 실행한다."""
import runpy, sys
from pathlib import Path
sys.exit(runpy.run_path(str(Path(__file__).resolve().parent / "verify_W38_misc_cycle48.py"), run_name="__main__") and 0)
