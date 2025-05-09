import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/ecommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OAuth Config
    OAUTH2_PROVIDERS = {
        'auth0': {
            'client_id': os.environ.get('AUTH0_CLIENT_ID'),
            'client_secret': os.environ.get('AUTH0_CLIENT_SECRET'),
            'server_metadata_url': os.environ.get('AUTH0_DOMAIN') + '/.well-known/openid-configuration',
            'client_kwargs': {
                'scope': 'openid profile email'
            }
        }
    }
    
    # Africa's Talking Config
    AFRICAS_TALKING_API_KEY = os.environ.get('AFRICAS_TALKING_API_KEY')
    AFRICAS_TALKING_USERNAME = os.environ.get('AFRICAS_TALKING_USERNAME')
    AFRICAS_TALKING_SENDER_ID = os.environ.get('AFRICAS_TALKING_SENDER_ID')