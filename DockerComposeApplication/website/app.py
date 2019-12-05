from requests import get
from flask import Flask

app = Flask(__name__)

# Docker-compose created a virtual network among the container, their host
# name matches their service name.
PRODUCTS_API_URL = 'http://products-service'


@app.route('/')
def index():
    return 'Welcome to shop!'


@app.route('/products')
def products():
    """
    This app will communicate with products API.
    """
    # Make a request to products service
    try:
        return get(PRODUCTS_API_URL).json()
    except ConnectionError:
        return 'Products service is not available.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
