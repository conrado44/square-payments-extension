# Square Payments Extension

## Environment Setup

### Using UV (Recommended)

UV is a fast Python package installer and resolver recommended for Block/Square projects.

1. Install the extension using the provided script:
   ```bash
   ./install_uv.sh
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

### Using pip (Legacy)

If you prefer using pip:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the extension:
   ```bash
   pip install -e .
   ```

## Environment Variables

This extension requires the following environment variables to be set:

```
SQUARE_APPLICATION_ID=your_application_id_here
SQUARE_LOCATION_ID=your_location_id_here
SQUARE_ACCESS_TOKEN=your_access_token_here
```

You can set these environment variables in your system or create a `.env` file (do not commit this file to version control).

## Security Notice

Never commit sensitive credentials directly in your code or configuration files. Always use environment variables for sensitive information.

If you've accidentally committed credentials, follow these steps:
1. Revoke the exposed credentials in the Square Developer Dashboard
2. Generate new credentials
3. Update your environment variables with the new credentials
4. Make sure your `.env` file is in your `.gitignore`