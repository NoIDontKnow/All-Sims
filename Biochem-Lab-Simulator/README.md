# Biochem Lab Simulator

Simulates titration curves (strong/strong, weak/strong) and a simple 1D diffusion demo.

## Features
- Titration simulator with adjustable acid/base concentration and volumes
- Calculates pH using appropriate formulas (Henderson-Hasselbalch for weak acid)
- Plot titration curve and show equivalence point
- 1D diffusion demo visualizing concentration over time

## Run
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Notes
- This is an educational simulator and uses simplified chemical approximations.
- Values are in molarity (M) and volumes in mL in the UI.
