#!/usr/bin/env python3
"""Compatibility entry point for the attestation-gated reasoning eval engine.

The canonical implementation lives in reasoning_eval_engine.py. Keeping this
small entry point preserves existing CLI paths while preventing a legacy runner
from bypassing target-execution receipt requirements.
"""
from reasoning_eval_engine import main


if __name__ == "__main__":
    raise SystemExit(main())
