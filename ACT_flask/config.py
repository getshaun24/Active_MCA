class Config(object):
    """Base config, uses staging database server."""

    # Mongo config
    MONGO_DB='Active_MCA'


    # Plaid config
    # Get your Plaid API keys from the dashboard: https://dashboard.plaid.com/account/keys
    PLAID_CLIENT_ID='xxx'
    PLAID_SECRET='xxx'
    # Use 'sandbox' to test with fake credentials in Plaid's Sandbox environment
    # Use 'development' to test with real credentials while developing
    # Use 'production' to go live with real users
    PLAID_ENV='sandbox'
    # PLAID_PRODUCTS is a comma-separated list of products to use when
    # initializing Link, e.g. PLAID_PRODUCTS=auth,transactions.
    # see https://plaid.com/docs/api/tokens/#link-token-create-request-products for a complete list
    PLAID_PRODUCTS=['auth','transactions','identity']
    # PLAID_COUNTRY_CODES is a comma-separated list of countries to use when
    # initializing Link, e.g. PLAID_COUNTRY_CODES=US,CA.
    # see https://plaid.com/docs/api/tokens/#link-token-create-request-country-codes for a complete list
    PLAID_COUNTRY_CODES=['US']
    # Only required for OAuth:
    # Set PLAID_REDIRECT_URI to 'http://localhost:3000'
    # The OAuth redirect flow requires an endpoint on the developer's website
    # that the bank website should redirect to. You will need to configure
    # this redirect URI for your client ID through the Plaid developer dashboard
    # at https://dashboard.plaid.com/team/api.
    PLAID_REDIRECT_URI=None

    APP_URL='http://127.0.0.1:5000'

    # Change this to your email when you are developing
    EMAIL_LIST='reidkostenukdev@gmail.com'

class ProductionConfig(Config):
    # Plaid production config
    ENV='production'
    PLAID_ENV='production'

    """ We should probably have a production and development mongo environment as well"""

    APP_URL='https://www.activemca.com'

class DevelopmentConfig(Config):
    # Plaid production config
    # PLAID_ENV='development'

    ENV='development'
    TEMPLATES_AUTO_RELOAD=True

    
