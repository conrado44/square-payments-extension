# Square Payments Extension for Goose

This extension allows Goose to handle payment card entry using Square's Web Payments SDK. It provides tools for:

1. Creating customer records in Square
2. Displaying a card entry form using Square's Web Payments SDK
3. Creating cards on file for customers

## Installation

```bash
pip install -e .
```

## Configuration

Add the following to your Goose configuration:

```yaml
extensions:
  square_payments:
    application_id: "your_application_id"
    location_id: "your_location_id"
```

## Usage

The extension provides three main tools:

1. `create_customer` - Creates a new customer record in Square
2. `show_card_form` - Displays the Square Web Payments SDK card entry form
3. `create_card_on_file` - Creates a card on file for a customer using a tokenized card

Example workflow:

```python
# Create a customer
customer_result = goose.use_tool("create_customer", {
    "given_name": "John",
    "family_name": "Doe",
    "email_address": "john.doe@example.com"
})

# Show card form
form_result = goose.use_tool("show_card_form")

# After card tokenization, create card on file
card_result = goose.use_tool("create_card_on_file", {
    "customer_id": customer_result.data["customer_id"],
    "source_id": form_result.data["source_id"]
})
```

## Development

This extension is built to work with the Square Web Payments SDK in the sandbox environment. For production use, update the SDK URL and ensure proper error handling.