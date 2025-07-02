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

### Environment Variables (Recommended)

For security, it's recommended to use environment variables for your Square credentials:

```bash
export SQUARE_APPLICATION_ID="your_application_id"
export SQUARE_LOCATION_ID="your_location_id"
export SQUARE_ACCESS_TOKEN="your_access_token"
```

You can also create a `.env` file (make sure to add it to `.gitignore`) and load it using a library like `python-dotenv`.

### Configuration File

Add the following to your Goose configuration:

```yaml
extensions:
  square_payments:
    application_id: "${SQUARE_APPLICATION_ID}"
    location_id: "${SQUARE_LOCATION_ID}"
    access_token: "${SQUARE_ACCESS_TOKEN}"
```

This will use the environment variables you've set.

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

## Security Best Practices

1. **Never commit sensitive credentials** directly in your code or configuration files.
2. Always use environment variables for sensitive information.
3. Add `.env` files to your `.gitignore` to prevent accidental commits.
4. Regularly rotate your access tokens.
5. If you suspect a token has been exposed:
   - Immediately revoke the token in the Square Developer Dashboard
   - Generate a new token
   - Update your environment variables with the new token