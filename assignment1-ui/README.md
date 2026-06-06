# Assignment 1 — SauceDemo UI Automation (Python)

End-to-end UI tests for https://www.saucedemo.com/ using **pytest + Playwright (Python)** with the
**Page Object Model**.

## What's covered

- **Positive:** valid login, logout, add to cart, multi-item cart, sorting (low→high / high→low).
- **Negative:** locked-out user, wrong password, unknown user, empty username/password,
  checkout blocked on missing fields.
- **End to end:** login → add products → cart → checkout info → review → finish → order confirmation.

Tests are marked `positive`, `negative`, `e2e`, `ui` so they can be filtered:

```bash
pytest assignment1-ui -m negative
```

## Layout

```
assignment1-ui/
├── pages/              # LoginPage, InventoryPage, CartPage, CheckoutPage (Page Object Model)
├── ui_data.py          # users, products, checkout data
├── conftest.py         # fixtures: login_page, inventory_page, logged_in_inventory
├── tests/              # test_login_positive / test_login_negative / test_cart / test_checkout_e2e
└── test-cases/         # SauceDemo_Manual_TestCases.csv  (Excel/Sheets ready)
```

## Manual test cases

`test-cases/SauceDemo_Manual_TestCases.csv` — open directly in Excel or Google Sheets.
Mandatory columns included: **Severity, Priority, Steps, Expected, Actual, Status**
(plus Test Case ID, Module, Scenario Type, Title, Preconditions).

## Run

```bash
pytest assignment1-ui                 # headless (default)
pytest assignment1-ui --headed        # watch the browser
pytest assignment1-ui --browser firefox
```

## Framework choice + why

**pytest + Playwright (Python), Page Object Model.**
- Playwright's auto-waiting locators (using SauceDemo's `data-test` hooks) keep tests stable.
- POM centralises selectors, so UI changes need a single-file fix.
- The pytest plugin gives the `page` fixture, headed/headless switches, multi-browser support, and
  trace/screenshot/video on failure for fast triage.

## Extension plan (parallelisation / reporting)

- **Parallelisation:** `pytest -n auto` (pytest-xdist) runs tests across CPU cores; add
  `--browser firefox --browser webkit` for a cross-browser matrix and shard across CI runners.
- **Reporting:** `pytest-html` report today; can add Allure for history/trends and publish to the
  GitHub Actions job summary.
- **Next:** visual regression via Playwright's `expect(page).to_have_screenshot()`, and a
  smoke-vs-regression marker split for fast PR feedback.
