# HeapSentinel: Differential Memory Velocity Tracer

A zero-overhead statistical allocation tracer that detects compounding object retention leaks in production before Out-Of-Memory (OOM) fatal kills.

## Features
- **Differential Rate Analysis:** Evaluates first-order allocation velocity over rolling execution windows.
- **Non-Intrusive:** Operates without continuous heap walking or process pauses.
- **Configurable Early Alerts:** Sets proactive threshold warnings based on accumulation rates.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com
