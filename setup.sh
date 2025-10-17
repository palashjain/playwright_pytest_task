#!/bin/bash

# Setup script for Playwright Pytest Framework
# Handles virtual environment creation and dependency installation

echo "========================================="
echo "Playwright Pytest Framework Setup"
echo "========================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists!"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "❌ Failed to activate virtual environment!"
    echo "Please check your Python installation and try again."
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo ""

# Install dependencies with error handling
echo "📥 Installing dependencies..."
if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo ""
    echo "🔧 Troubleshooting steps:"
    echo "1. Check your internet connection"
    echo "2. Try installing dependencies one by one:"
    echo "   pip install playwright==1.40.0"
    echo "   pip install pytest==7.4.3"
    echo "   pip install pytest-playwright==0.4.3"
    echo "   pip install allure-pytest==2.13.2"
    echo "   pip install pytest-html==4.1.1"
    echo ""
    echo "3. If you encounter greenlet issues, try:"
    echo "   pip install greenlet==2.0.2"
    echo ""
    exit 1
fi

echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
if command -v playwright &> /dev/null; then
    playwright install chromium
    echo "✅ Playwright browsers installed"
else
    echo "⚠️  Playwright command not found, trying alternative installation..."
    python -m playwright install chromium
fi

echo ""

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs screenshots downloads allure-results

echo ""

# Verify installation
echo "✅ Verifying installation..."
python3 -c "import pytest; print('Pytest version:', pytest.__version__)" || echo "❌ Pytest import failed"
python3 -c "import allure; print('Allure-pytest installed successfully')" || echo "❌ Allure import failed"

echo ""
echo "========================================="
echo "✅ Setup completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Virtual environment is already activated"
echo ""
echo "2. Update configuration if needed:"
echo "   config/config.ini"
echo ""
echo "3. Run tests:"
echo "   pytest"
echo ""
echo "4. View Allure report:"
echo "   allure serve allure-results"
echo ""
echo "Happy Testing! 🚀"
echo ""

# Keep the terminal open for the user
echo "📝 Terminal commands available:"
echo "   deactivate    # Exit virtual environment"
echo "   source venv/bin/activate    # Re-activate later"
echo "   pytest    # Run tests"
echo ""
