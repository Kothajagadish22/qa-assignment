# Manual Test Cases — SauceDemo (Assignment 1)

These are the **manual** test cases the assignment asks for (Positive, Negative, End to End).

## Files

| File | Use |
|------|-----|
| `SauceDemo_Manual_TestCases.xlsx` | **Open in Excel** — 4 sheets: All, Positive, Negative, E2E |
| `SauceDemo_Manual_TestCases.csv` | Same data — import into **Google Sheets** |

## Mandatory columns (included)

- **Severity**
- **Priority**
- **Steps**
- **Expected**
- **Actual**
- **Status**

Plus: Test Case ID, Module, Scenario Type, Title, Preconditions.

## Counts

| Scenario Type | Count | Examples |
|---------------|-------|----------|
| **Positive** | 10 | Valid login, add to cart, sort products, complete checkout |
| **Negative** | 7 | Locked user, wrong password, empty fields, checkout errors |
| **End to End** | 2 | Full purchase journey, cart persists across navigation |

## Upload to Google Sheets

1. Go to [sheets.google.com](https://sheets.google.com) → **Blank spreadsheet**
2. **File → Import → Upload**
3. Choose `SauceDemo_Manual_TestCases.csv` (or `.xlsx`)
4. Import location: **Replace spreadsheet** or **Insert new sheet(s)**

Or open the `.xlsx` in Excel and copy/paste each sheet into Google Sheets.

## Regenerate Excel

```bash
python assignment1-ui/test-cases/generate_excel.py
```
