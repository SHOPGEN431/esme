#!/usr/bin/env python3
"""
WSGI entry point for ESME LLC Directory
Optimized for production deployment
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import config

# Load configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# Production optimizations
if config_name == 'production':
    # Enable gzip compression
    from flask_compress import Compress
    Compress(app)
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        headers = config['production'].SECURITY_HEADERS
        for header, value in headers.items():
            response.headers[header] = value
        return response
    
    # Cache static files
    @app.after_request
    def add_cache_headers(response):
        if response.status_code == 200:
            if 'static' in request.path:
                response.cache_control.max_age = 31536000  # 1 year
                response.cache_control.public = True
            else:
                response.cache_control.max_age = 300  # 5 minutes
        return response

if __name__ == '__main__':
    app.run()
