class Config(object):
    """Base config, uses staging database server."""

    # Mongo config
    MONGO_CLI='mongodb+srv://Gr33nworldwid31:Gr33nworldwid31@activemca-1.ugg7j.mongodb.net/'
    MONGO_DB='Active_MCA'

    # Mail server config
    MAIL_SERVER='smtp.fastmail.com'
    MAIL_PORT=465
    MAIL_USERNAME='getresources@fastmail.com'
    MAIL_PASSWORD='6a2bc25t2bjd6v3l'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True

    # Sign now config
    SIGNNOW_ID='5e2ad8499ceb129ce75fdb712acaad38'
    SIGNNOW_SERCRET='166b8bbc12932f68fd0f98a18bc078f7'
    SIGNNOW_USERNAME='shaun@thisisget.com'
    SIGNNOW_PASS='Gr33nworldwid31!'
    SIGNNOW_BASIC_AUTH='NWUyYWQ4NDk5Y2ViMTI5Y2U3NWZkYjcxMmFjYWFkMzg6MTY2YjhiYmMxMjkzMmY2OGZkMGY5OGExOGJjMDc4Zjc='
    SIGNNOW_ENV='sandbox'

    # Ocrolus config
    OCROLUS_ID='oFnOBT3NvYCuLLKoAp55Nz9ZwuGDxmMh'
    OCROLUS_SECRET='YK0Ub1qs3K3_yvQCA3hY2F8eAyhWICslblwAlgH_FspwhxSnUTTw97ayNtKllSgl'

    # Plaid config
    # Get your Plaid API keys from the dashboard: https://dashboard.plaid.com/account/keys
    PLAID_CLIENT_ID='606cb393292928000fb2ddf0'
    PLAID_SECRET='3822a53bd8778bf391610496f22b82'
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

    # Dwolla config
    DWOLLA_APP_KEY = 'TdDkARwsDT2r1eHIRWv7k0sQ03xKng485hKAsIsHvxKjOPyG6f'
    DWOLLA_APP_SECRET = 'nEP5EcAsPmTK3qrjcqhCPQnQxKSlx39guxQXNNzZkB8MVllUBO'
    DWOLLA_APP_ENV='sandbox'
    DWOLLA_APP_URL='https://api-sandbox.dwolla.com'
    DWOLLA_MASTER_RECIPIENTS='reidkostenukdev@gmail.com'

    # Other configurations
    SESSION_PERMANENT=False
    SESSION_TYPE='filesystem'

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

    