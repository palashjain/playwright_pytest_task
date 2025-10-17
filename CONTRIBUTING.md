# Contributing to Playwright Pytest Framework

Thank you for your interest in contributing to this automation framework!

## Development Guidelines

### Adding New Page Objects

1. Create a new file in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class variables
4. Implement page-specific methods

Example:
```python
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure


class NewPage(BasePage):
    """
    Page Object for New Page.
    Handles new page operations.
    """
    
    # Locators
    ELEMENT_LOCATOR = "selector"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger.info("New page initialized")
    
    @allure.step("Perform action")
    def perform_action(self) -> None:
        """Perform specific action."""
        self.click(self.ELEMENT_LOCATOR)
        self.logger.info("Action performed")
```

### Adding New Tests

1. Create test file in `tests/` directory
2. Use fixtures from `conftest.py`
3. Follow AAA pattern (Arrange, Act, Assert)
4. Add Allure annotations
5. Use proper assertions

Example:
```python
import pytest
import allure
from playwright.sync_api import Page


@allure.feature("Feature Name")
@allure.story("Story Name")
class TestNewFeature:
    
    @allure.title("Test Title")
    @allure.description("Test description")
    def test_new_feature(self, page: Page, new_page):
        """Test new feature."""
        # Arrange
        new_page.navigate_to_page()
        
        # Act
        new_page.perform_action()
        
        # Assert
        assert new_page.is_action_successful()
```

### Adding New Fixtures

1. Add fixtures to `conftest.py`
2. Use appropriate scope (function, class, module, session)

### Adding Utilities

1. Create utility functions in `utils/helpers.py`
2. Or create new utility module in `utils/` directory
3. Keep utilities **generic** and **reusable**

### Logging

Always add logging to track test execution:

```python
self.logger.info("Information message")
self.logger.debug("Debug message")
self.logger.warning("Warning message")
self.logger.error("Error message")
```

### Configuration

Add new configuration in `config/config.ini`:

```ini
[SECTION]
key = value
```

Access in code:
```python
value = self.config.get('SECTION', 'key')
```

## Testing Your Changes

Before submitting:

1. Run all tests: `pytest`
2. Check logs for errors: `logs/test_execution.log`
3. Verify Allure report: `allure serve allure-results`
4. Ensure no pylint warnings

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Update documentation (README.md)
5. Ensure all tests pass
6. Submit pull request with clear description

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Review similar implementations
3. Contact the team

Thank you for contributing! 🚀
