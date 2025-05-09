from flask import redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import create_access_token
from app import oauth

def setup_oauth(app):
    auth0 = oauth.register(
        'auth0',
        client_id=app.config['OAUTH2_PROVIDERS']['auth0']['client_id'],
        client_secret=app.config['OAUTH2_PROVIDERS']['auth0']['client_secret'],
        api_base_url=app.config['OAUTH2_PROVIDERS']['auth0']['api_base_url'],
        access_token_url=app.config['OAUTH2_PROVIDERS']['auth0']['access_token_url'],
        authorize_url=app.config['OAUTH2_PROVIDERS']['auth0']['authorize_url'],
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('auth_callback', _external=True)
    )

@app.route('/callback')
def auth_callback():
    token = oauth.auth0.authorize_access_token()
    session['user'] = token
    access_token = create_access_token(identity=token['userinfo']['email'])
    return redirect(url_for('frontend') + f'#token={access_token}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        'https://' + app.config['AUTH0_DOMAIN']
        + '/v2/logout?'
        + urlencode({
            'returnTo': url_for('frontend', _external=True),
            'client_id': app.config['AUTH0_CLIENT_ID'],
        }, quote_via=quote_plus)
    )