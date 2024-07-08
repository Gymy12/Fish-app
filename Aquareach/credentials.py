PHONE_NUMBER = "0704439347"

# M-Pesa Credentials
MPESA_CONSUMER_KEY = "d1rAqX0MgQZVi5gNs727XY0zGCckX5eQCR9N33qMbBrG2O7j"
MPESA_CONSUMER_SECRET = "mGn6fdyu8K4vDqz7JSWISFvMlEIB7E7iGnqwrNkZkzFal3LXR69rK1A5z1EewgGb"
MPESA_SHORTCODE = "600988"

# Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# This is only used on sandbox, do not set this variable in production
# For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

MPESA_EXPRESS_SHORTCODE = "174379"

# Type of shortcode
# Possible values:
# - paybill (For Paybill)
# - till_number (For Buy Goods Till Number)

MPESA_SHORTCODE_TYPE = "paybill"

# Lipa na MPESA Online passkey
# Sandbox passkey is available on test credentials page
# Production passkey is sent via email once you go live

MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_USERNAME = "testapi"

# Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

MPESA_INITIATOR_SECURITY_CREDENTIAL = "Safaricom999!*!"
