from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from flask_compress import Compress
import pandas as pd
import os

app = Flask(__name__)

# Enable compression
Compress(app)

# Configure caching
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})
cache.init_app(app)

# Load LLC services data
def load_services_data():
    # Get all states from CSV
    all_states = get_all_states()
    
    services = [
        {
            'name': 'Northwestern',
            'slug': 'northwestern',
            'pricing': '$39 formation service',
            'description': 'Northwest Registered Agent offers the most cost-effective LLC formation service at just $39, with comprehensive business formation packages including free registered agent service.',
            'features': [
                'Free registered agent service',
                'Business address & email included',
                'Custom website & domain name',
                'Operating agreement',
                'EIN application assistance'
            ],
            'states': all_states,
            'website': 'https://consumer-champion.org/LLCwebsite',
            'rating': 4.8,
            'reviews': 1250,
            'recommended': True,
            'pros': ['Lowest price at $39', 'Free registered agent service', 'Comprehensive package', 'Excellent customer service', 'Privacy protection'],
            'cons': ['Limited additional services', 'No attorney consultations', 'Basic website builder']
        },
        {
            'name': 'LegalZoom',
            'slug': 'legalzoom',
            'pricing': 'Starting at $79 + state fees',
            'description': 'LegalZoom is a well-established legal services company offering comprehensive LLC formation packages with additional legal document services.',
            'features': [
                'Operating agreement included',
                'EIN application assistance',
                'Business compliance alerts',
                'Legal document library',
                'Attorney consultations'
            ],
            'states': all_states,
            'website': 'https://www.legalzoom.com',
            'rating': 4.6,
            'reviews': 2100,
            'pros': ['Well-established brand', 'Attorney consultations', 'Comprehensive legal services', 'Trusted by millions', 'Additional legal documents'],
            'cons': ['Higher pricing', 'Upselling tactics', 'Complex pricing structure']
        },
        {
            'name': 'Rocket Lawyer',
            'slug': 'rocket-lawyer',
            'pricing': '$99.99/month subscription',
            'description': 'Rocket Lawyer offers a subscription-based legal service model with unlimited legal documents and attorney consultations.',
            'features': [
                'Unlimited legal documents',
                'Attorney consultations',
                'Business formation included',
                'Document review services',
                'Legal health score'
            ],
            'states': all_states,
            'website': 'https://www.rocketlawyer.com',
            'rating': 4.5,
            'reviews': 1800,
            'pros': ['Unlimited legal documents', 'Attorney consultations', 'Subscription model', 'Document review services', 'Legal health monitoring'],
            'cons': ['Monthly subscription required', 'Higher long-term cost', 'May be overkill for simple needs']
        },
        {
            'name': 'Incfile',
            'slug': 'incfile',
            'pricing': 'Starting at $0 + state fees',
            'description': 'Incfile offers competitive pricing with a focus on simplicity and ease of use for LLC formation.',
            'features': [
                'Free LLC formation',
                'Free registered agent for 1 year',
                'Operating agreement',
                'Business compliance alerts',
                'Tax consultation'
            ],
            'states': all_states,
            'website': 'https://www.incfile.com',
            'rating': 4.7,
            'reviews': 1650,
            'pros': ['Free formation service', 'Free registered agent for 1 year', 'Simple pricing', 'Good customer support', 'Tax consultation included'],
            'cons': ['Limited features in free plan', 'Upselling to paid plans', 'Basic service offerings']
        },
        {
            'name': 'ZenBusiness',
            'slug': 'zenbusiness',
            'pricing': 'Starting at $0 + state fees',
            'description': 'ZenBusiness offers a unique $0 LLC formation service with ongoing business support and compliance monitoring.',
            'features': [
                'Free LLC formation',
                'Free registered agent for 1 year',
                'Compliance monitoring',
                'Business credit building',
                'Website builder'
            ],
            'states': all_states,
            'website': 'https://www.zenbusiness.com',
            'rating': 4.9,
            'reviews': 1950,
            'pros': ['Free formation service', 'Ongoing business support', 'Compliance monitoring', 'Business credit building', 'Website builder'],
            'cons': ['Limited free features', 'Upselling to paid plans', 'May be overwhelming for simple needs']
        },
        {
            'name': 'Swyft Filings',
            'slug': 'swyft-filings',
            'pricing': 'Starting at $49 + state fees',
            'description': 'Swyft Filings offers fast and reliable LLC formation services with excellent customer support and competitive pricing.',
            'features': [
                'Fast processing times',
                'Free registered agent for 1 year',
                'Operating agreement',
                'Business compliance alerts',
                'Customer support'
            ],
            'states': all_states,
            'website': 'https://www.swyftfilings.com',
            'rating': 4.4,
            'reviews': 1200,
            'pros': ['Fast processing', 'Competitive pricing', 'Good customer support', 'Free registered agent', 'Simple process'],
            'cons': ['Limited additional services', 'Basic features', 'No attorney consultations']
        },
        {
            'name': 'MyCorporation',
            'slug': 'mycorporation',
            'pricing': 'Starting at $99 + state fees',
            'description': 'MyCorporation provides comprehensive business formation services with a focus on education and guidance.',
            'features': [
                'Educational resources',
                'Operating agreement',
                'EIN application assistance',
                'Business compliance alerts',
                'Customer support'
            ],
            'states': all_states,
            'website': 'https://www.mycorporation.com',
            'rating': 4.3,
            'reviews': 950,
            'pros': ['Educational resources', 'Comprehensive guidance', 'Good customer support', 'Established company', 'Clear pricing'],
            'cons': ['Higher pricing', 'Limited features', 'No free options']
        },
        {
            'name': 'BizFilings',
            'slug': 'bizfilings',
            'pricing': 'Starting at $99 + state fees',
            'description': 'BizFilings offers professional business formation services with a focus on compliance and ongoing support.',
            'features': [
                'Compliance monitoring',
                'Operating agreement',
                'EIN application assistance',
                'Business compliance alerts',
                'Professional support'
            ],
            'states': all_states,
            'website': 'https://www.bizfilings.com',
            'rating': 4.2,
            'reviews': 800,
            'pros': ['Professional service', 'Compliance focus', 'Ongoing support', 'Established company', 'Reliable service'],
            'cons': ['Higher pricing', 'Limited features', 'No free options', 'Basic service offerings']
        },
        {
            'name': 'CorpNet',
            'slug': 'corpnet',
            'pricing': 'Starting at $89 + state fees',
            'description': 'CorpNet provides comprehensive business formation and compliance services with personalized support.',
            'features': [
                'Personalized support',
                'Operating agreement',
                'EIN application assistance',
                'Compliance monitoring',
                'Business consulting'
            ],
            'states': all_states,
            'website': 'https://www.corpnet.com',
            'rating': 4.1,
            'reviews': 750,
            'pros': ['Personalized support', 'Comprehensive services', 'Business consulting', 'Compliance focus', 'Professional service'],
            'cons': ['Higher pricing', 'Limited online features', 'No free options', 'May be overkill for simple needs']
        },
        {
            'name': 'Harbor Compliance',
            'slug': 'harbor-compliance',
            'pricing': 'Starting at $99 + state fees',
            'description': 'Harbor Compliance specializes in business compliance and formation services with a focus on ongoing support.',
            'features': [
                'Compliance expertise',
                'Operating agreement',
                'EIN application assistance',
                'Ongoing compliance monitoring',
                'Professional support'
            ],
            'states': all_states,
            'website': 'https://www.harborcompliance.com',
            'rating': 4.0,
            'reviews': 600,
            'pros': ['Compliance expertise', 'Ongoing support', 'Professional service', 'Comprehensive monitoring', 'Reliable service'],
            'cons': ['Higher pricing', 'Limited features', 'No free options', 'May be complex for simple needs']
        }
    ]
    return services

# Load local businesses data from CSV
def load_local_businesses():
    csv_path = r"C:\Users\webd5\Downloads\LLC Data.csv"
    try:
        df = pd.read_csv(csv_path)
        # Clean the us_state column - remove NaN values and convert to string
        df['us_state'] = df['us_state'].astype(str)
        df['us_state'] = df['us_state'].replace('nan', '')
        df['us_state'] = df['us_state'].replace('NaN', '')
        # Filter out rows with empty state values
        df = df[df['us_state'].str.strip() != '']
        return df.to_dict('records')
    except FileNotFoundError:
        # Return sample data if CSV doesn't exist
        return [
            {
                'name': 'ABC Legal Services',
                'us_state': 'California',
                'city': 'Los Angeles',
                'full_address': '123 Business St, Los Angeles, CA 90210',
                'phone': '(555) 123-4567',
                'rating': 4.5,
                'reviews': 25,
                'site': 'https://example.com',
                'subtypes': 'LLC formation, Legal services'
            },
            {
                'name': 'Texas Business Solutions',
                'us_state': 'Texas',
                'city': 'Houston',
                'full_address': '456 Commerce Ave, Houston, TX 77001',
                'phone': '(555) 234-5678',
                'rating': 4.3,
                'reviews': 18,
                'site': 'https://example.com',
                'subtypes': 'LLC formation, Business consulting'
            }
        ]

# Get all unique states from CSV
def get_all_states():
    csv_path = r"C:\Users\webd5\Downloads\LLC Data.csv"
    try:
        df = pd.read_csv(csv_path)
        # Clean the us_state column - remove NaN values and convert to string
        df['us_state'] = df['us_state'].astype(str)
        df['us_state'] = df['us_state'].replace('nan', '')
        df['us_state'] = df['us_state'].replace('NaN', '')
        # Get unique states, filter out empty strings, and sort them alphabetically
        states = sorted([state for state in df['us_state'].unique().tolist() if state.strip()])
        return states
    except FileNotFoundError:
        # Return default states if CSV doesn't exist
        return ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']

# Get services by state
def get_services_by_state(state_name):
    services = load_services_data()
    return [service for service in services if state_name in service['states']]

# Get local businesses by state
def get_local_businesses_by_state(state_name):
    businesses = load_local_businesses()
    return [business for business in businesses if business['us_state'].lower() == state_name.lower()]

@app.route('/')
@cache.cached(timeout=300)
def index():
    services = load_services_data()
    states = get_all_states()
    return render_template('index.html', services=services, states=states)

@app.route('/services/<service_slug>')
@cache.memoize(timeout=300)
def service_page(service_slug):
    services = load_services_data()
    service = next((s for s in services if s['slug'] == service_slug), None)
    
    if not service:
        return "Service not found", 404
    
    return render_template('service.html', service=service)

@app.route('/services/<service_slug>/<state_name>')
def service_state_page(service_slug, state_name):
    services = load_services_data()
    service = next((s for s in services if s['slug'] == service_slug), None)
    
    if not service:
        return "Service not found", 404
    
    if state_name not in service['states']:
        return "State not available for this service", 404
    
    local_businesses = get_local_businesses_by_state(state_name)
    
    return render_template('service_state.html', 
                         service=service, 
                         state_name=state_name,
                         local_businesses=local_businesses)

@app.route('/states/<state_name>')
@cache.memoize(timeout=300)
def state_page(state_name):
    services = get_services_by_state(state_name)
    local_businesses = get_local_businesses_by_state(state_name)
    
    if not services and not local_businesses:
        return "State not found", 404
    
    return render_template('state.html', 
                         state_name=state_name, 
                         services=services, 
                         local_businesses=local_businesses)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/locations')
@cache.cached(timeout=300)
def locations():
    services = load_services_data()
    states = get_all_states()
    return render_template('locations.html', services=services, states=states)

@app.route('/sitemap.xml')
def sitemap():
    services = load_services_data()
    states = get_all_states()
    
    sitemap_content = render_template('sitemap.xml', services=services, states=states)
    response = app.response_class(sitemap_content, mimetype='application/xml')
    return response

if __name__ == '__main__':
    app.run(debug=True)
