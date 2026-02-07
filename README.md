# Thermodynamic Property & Process Calculator

Professional-grade engineering tool for thermodynamic calculations.

## Features

- **Property Calculations**: Water/steam, air, refrigerants (R-134a, R-22, CO2)
- **Process Analysis**: Isentropic, isobaric, isochoric, throttling, polytropic
- **CLI Interface**: Command-line tools for quick calculations
- **Web UI**: Browser-based interface
- **Export**: JSON, CSV, Markdown reports
- **Plotting**: T-s and P-h diagrams

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start

### Property Lookup
```bash
python -m src.cli property --fluid water --temp 100 --pressure 101.325
```

### Process Analysis
```bash
python -m src.cli process --fluid air --inlet-temp 25 --inlet-pressure 100 --outlet-pressure 800 --efficiency 0.85
```

### Interactive Mode
```bash
python -m src.cli interactive
```

## Supported Fluids

- Water/Steam
- Air
- R-134a
- R-22
- CO2

## Units

- Temperature: °C
- Pressure: kPa
- Enthalpy: kJ/kg
- Entropy: kJ/kg-K
- Specific Volume: m³/kg

## Documentation

See `docs/USER_GUIDE.md` for detailed usage instructions.

## Testing
```bash
pytest
```

## License

MIT
