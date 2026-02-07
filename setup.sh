#!/bin/bash

echo "🚀 Setting up Thermodynamic Calculator..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate and install
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the calculator:"
echo "1. Activate: source venv/bin/activate"
echo "2. Run: python -m src.cli property --fluid water --temp 100 --pressure 101.325"
echo ""
