# Square Payments Extension

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