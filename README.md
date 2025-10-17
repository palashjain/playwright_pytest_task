# Playwright Python Pytest Automation Framework

## Overview

This is UI automation framework built using **Playwright**, **Python**, **Pytest**, and **Allure** for reporting.

## Framework Architecture

### Folder Structure

```
playwright_pytest_task/
├── config/
│   └── config.ini              # Configuration file for application settings
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Base page with common methods
│   ├── login_page.py           # Login page object
│   ├── home_page.py            # Home/Navigation page object
│   ├── store_list_page.py      # Store listing page object
│   ├── store_details_page.py   # Store details page object
│   └── create_polygon_page.py  # Create/Edit polygon page object
├── tests/
│   ├── __init__.py
│   └── test_polygon_management.py  # Polygon management test scenarios
├── utils/
│   ├── __init__.py
│   ├── config_manager.py       # Configuration management (Singleton)
│   ├── logger.py               # Logging utility (Singleton)
│   ├── browser_manager.py      # Browser lifecycle management (Singleton)
│   └── helpers.py              # Helper utilities
├── testData/
│   └── lat_long_coordinates.csv    # Test data CSV for polygon creation
├── conftest.py                 # Pytest fixtures and configuration
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome browser (tests run on Chrome only for now)

## Installation

### 1. Clone or Download the Project

```bash
cd playwright_pytest_task
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### OR do quick setup

```bash
./setup.sh
```

## Configuration

Edit the `config/config.ini` file to customize settings.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_polygon_management.py
```

### Run with Specific Markers

```bash
# Run only smoke tests
pytest -m smoke
```

### Run in Headless Mode

Edit `config/config.ini` and set `headless = true`, or run:

```bash
pytest --headed=false
```

## Viewing Test Reports

### Allure Reports

#### Generate and View Allure Report

```bash
allure serve allure-results
```

### Logs

Test execution logs are available in:
- `logs/test_YYYYMMDD_HHMMSS.log` - Individual test run logs

### Screenshots

Screenshots are captured on test failures and saved in:
- `screenshots/` directory

## Troubleshooting

### Common Issues

#### 1. Browser Not Found
```bash
# Install Playwright browsers
playwright install chromium
```

#### 2. Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Tests Failing
- Check if the application URL is accessible
- Verify credentials in `config/config.ini`
- Check logs in `logs/` directory
- Review screenshots in `screenshots/` directory

#### 4. Allure Report Not Generating
```bash
# Install Allure command-line tool
# macOS:
brew install allure
```

## Report Screenshot:

![alt text](<Report_screenshot_suite.png>)

![alt text](<Report_screenshot_test.png>)
