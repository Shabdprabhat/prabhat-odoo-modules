# Sale Order Line Fixed Discount

Apply fixed currency amount discounts directly on sale order lines.

## Overview

By default, Odoo only allows **percentage-based discounts** on sale order lines.
This module adds a **Fixed Discount Amount** field — so you can type in an exact
currency amount (e.g. *₹500 off* or *$20 off*) and Odoo automatically handles
the rest. The percentage is calculated for you. Works on both **Sale Orders**
and **Invoices**.

## Key Features

- **Fixed Discount Amount Field**: Enter an exact discount in your currency directly on each sale order line — no need to calculate percentages manually.
- **Auto Percentage Calculation**: Enter a fixed amount and the discount percentage is calculated automatically. Change the percentage and the amount updates too.
- **Visible in Table & Popup**: The Discount Amount column appears directly in the order lines table — no need to open each line individually.
- **Invoice Integration**: The fixed discount amount carries over to invoices/bills automatically, keeping your accounting accurate.
- **PDF Quotation Support**: Discount amounts print on the PDF quotation and invoice so your customers can clearly see the savings on each line.
- **Validation & Safety**: Built-in validation prevents the discount amount from exceeding the line total — no accidental negative prices.

## How It Works

1. **Install the Module**: Install from Apps. No extra configuration required.
2. **Open a Sale Order**: You will see a new "Discount Amt" column in the order lines table.
3. **Enter Fixed Discount**: Type the discount amount in your currency. The % discount field updates automatically.
4. **Confirm & Invoice**: Confirm the order. The discount flows to the invoice and prints on the PDF.

## Perfect For

- Giving a negotiated fixed discount to a customer (e.g. "₹500 off this order")
- Sales teams that think in amounts, not percentages
- Businesses where discounts are agreed in currency terms, not ratios
- Showing clear discount savings on customer-facing PDF quotations
- Keeping discount records accurate on invoices for accounting

## Technical Information

| Detail | Value |
|--------|-------|
| Odoo Version | 18.0 |
| Category | Sales |
| Dependencies | sale_management, account |
| License | LGPL-3 |
| Models Extended | sale.order.line, account.move.line |
| No Extra Configuration | Works immediately after install |

## Development

Developed by Prabhat Module.

For customizations, feature requests, or support — feel free to reach out.
Built with care for the Odoo Community.
