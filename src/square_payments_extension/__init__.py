"""Square Payments Extension for Goose."""

from typing import Any, Dict, List, Optional
from square.client import Client
from goose_core import Extension, Tool, ToolCall, ToolResult

class SquarePaymentsExtension(Extension):
    """Extension for handling Square Payments integration in Goose."""

    def __init__(self):
        super().__init__()
        self.application_id = None
        self.location_id = None
        self.access_token = None
        self.square_client = None

    def setup(self, config: Dict[str, Any]) -> None:
        """Set up the extension with configuration."""
        self.application_id = config.get('application_id')
        self.location_id = config.get('location_id')
        self.access_token = config.get('access_token')
        
        if not all([self.application_id, self.location_id, self.access_token]):
            raise ValueError("application_id, location_id, and access_token are required in config")
        
        # Initialize Square client
        self.square_client = Client(
            access_token=self.access_token,
            environment='sandbox'  # Change to 'production' for live environment
        )

    @Tool.tool("Create a customer record in Square")
    def create_customer(self, given_name: str, family_name: str, email_address: str) -> ToolResult:
        """
        Create a new customer in Square.
        
        Args:
            given_name: Customer's first name
            family_name: Customer's last name
            email_address: Customer's email address
            
        Returns:
            ToolResult containing the customer ID and status
        """
        try:
            result = self.square_client.customers.create_customer(
                body={
                    "given_name": given_name,
                    "family_name": family_name,
                    "email_address": email_address
                }
            )

            if result.is_success():
                return ToolResult(
                    success=True,
                    data={
                        "customer_id": result.body["customer"]["id"],
                        "created_at": result.body["customer"]["created_at"]
                    }
                )
            else:
                return ToolResult(
                    success=False,
                    error=f"Failed to create customer: {result.errors}"
                )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error creating customer: {str(e)}"
            )

    @Tool.tool("Show card entry form")
    def show_card_form(self) -> ToolResult:
        """
        Display the Square Web Payments SDK card entry form.
        
        Returns:
            ToolResult containing the HTML content for the card form
        """
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Card Entry Form</title>
            <script type="text/javascript" src="https://sandbox.web.squarecdn.com/v1/square.js"></script>
            <style>
                #payment-form {{
                    max-width: 550px;
                    margin: 20px auto;
                    padding: 20px;
                    border-radius: 4px;
                    background-color: #ffffff;
                }}
                
                #card-container {{
                    margin-bottom: 20px;
                    padding: 12px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }}
                
                button {{
                    background-color: #006aff;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 16px;
                    font-size: 16px;
                    cursor: pointer;
                    width: 100%;
                }}
                
                button:hover {{
                    background-color: #0055cc;
                }}
                
                #payment-status {{
                    margin-top: 20px;
                    padding: 10px;
                    border-radius: 4px;
                    display: none;
                }}
                
                .success {{
                    background-color: #d4edda;
                    color: #155724;
                }}
                
                .error {{
                    background-color: #f8d7da;
                    color: #721c24;
                }}
            </style>
        </head>
        <body>
            <form id="payment-form">
                <div id="card-container"></div>
                <button type="submit">Add Card</button>
                <div id="payment-status"></div>
            </form>
            
            <script>
                async function initializeCard() {{
                    const payments = Square.payments('{self.application_id}', '{self.location_id}');
                    const card = await payments.card();
                    await card.attach('#card-container');
                    
                    const form = document.getElementById('payment-form');
                    const statusDiv = document.getElementById('payment-status');
                    
                    form.addEventListener('submit', async (event) => {{
                        event.preventDefault();
                        
                        try {{
                            const result = await card.tokenize();
                            if (result.status === 'OK') {{
                                statusDiv.textContent = 'Card tokenized successfully';
                                statusDiv.className = 'success';
                                statusDiv.style.display = 'block';
                                
                                // Send the source ID to Goose
                                window.gooseCallback({{
                                    status: 'success',
                                    sourceId: result.token
                                }});
                            }}
                        }} catch (e) {{
                            statusDiv.textContent = e.message;
                            statusDiv.className = 'error';
                            statusDiv.style.display = 'block';
                            
                            window.gooseCallback({{
                                status: 'error',
                                error: e.message
                            }});
                        }}
                    }});
                }}
                
                window.onload = initializeCard;
            </script>
        </body>
        </html>
        '''
        return ToolResult(success=True, data={'html': html_content})

    @Tool.tool("Create card on file")
    def create_card_on_file(self, customer_id: str, source_id: str) -> ToolResult:
        """
        Create a card on file for a customer using a tokenized card source ID.
        
        Args:
            customer_id: The Square customer ID
            source_id: The tokenized card source ID from Web Payments SDK
            
        Returns:
            ToolResult containing the card on file details
        """
        try:
            result = self.square_client.cards.create_card(
                body={
                    "card": {
                        "customer_id": customer_id,
                        "source_id": source_id
                    },
                    "idempotency_key": f"card-{customer_id}-{source_id[:8]}"
                }
            )

            if result.is_success():
                return ToolResult(
                    success=True,
                    data={
                        "card_id": result.body["card"]["id"],
                        "card_brand": result.body["card"]["card_brand"],
                        "last_4": result.body["card"]["last_4"],
                        "exp_month": result.body["card"]["exp_month"],
                        "exp_year": result.body["card"]["exp_year"]
                    }
                )
            else:
                return ToolResult(
                    success=False,
                    error=f"Failed to create card on file: {result.errors}"
                )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error creating card on file: {str(e)}"
            )