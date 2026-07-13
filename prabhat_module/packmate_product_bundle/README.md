# PackMate - Product Bundle, Sales Kit and Combo Pack Manager

PackMate lets Odoo users sell one kit product while delivering the real component products through the standard sale and inventory flow.

## Features

- Mark any product as a PackMate kit, combo pack, or product bundle.
- Add multiple component products with quantities and UoM.
- Manual or automatic kit sales price calculation from components.
- Manual or automatic kit cost calculation from components.
- Add kit products to sale quotations as a single line.
- Expand kit components as priced sale order lines before confirmation.
- Use standard Odoo delivery orders for the real component products.
- Taxes from the kit line are automatically applied to component lines.

## Installation

1. Download the module and place it in your Odoo addons directory.
2. Restart the Odoo server.
3. Go to Apps > Update Apps List.
4. Search for "PackMate" and click Install.

## Configuration

1. Go to Sales > Configuration > PackMate Kits (or Products > PackMate Kits).
2. Create or edit a product and enable the **PackMate Kit** checkbox.
3. Add component products with quantities in the PackMate Components tab.
4. Choose a pricing mode (Manual or From Components) for sales and cost.

## Usage

### Creating a Kit Product

1. Go to Sales > Catalog > PackMate Kits.
2. Click Create and enable the PackMate Kit checkbox.
3. Add component products with quantities.
4. Set the pricing mode:
   - **Manual Price**: Set the kit price yourself.
   - **From Components**: Price is auto-calculated from component totals.
5. Save the product.

### Selling a Kit

1. Create a new quotation in the Sales app.
2. Add the PackMate kit product as a sale order line.
3. The kit appears as a single line on the quotation.
4. Click **Expand PackMate Kits** to split it into component lines (optional).
5. Confirm the order — component lines are created automatically.
6. Delivery orders are generated for the component products.

## Dependencies

- `sale` (Sales)
- `sale_stock` (Sales - Inventory)
- `product` (Product Management)

## License

LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

## Author

Prabhat
