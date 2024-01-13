from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

class CoreWebVitalsAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.crux_api_endpoint = 'https://chromeuxreport.googleapis.com/v1/records:queryRecord'

    def get_core_web_vitals(self, domains: list) -> dict:
        results = {}
        for domain in domains:
            metrics = ['largest_contentful_paint', 'first_input_delay', 'cumulative_layout_shift', 'first_contentful_paint', 'interaction_to_next_paint', 'experimental_time_to_first_byte']
            params = {
                'key': self.api_key,
                'url': f'https://{domain}',
                'metrics': metrics
            }
            response = requests.post(self.crux_api_endpoint, params=params)
            if response.status_code == 200:
                results[domain] = response.json()
            else:
                print(f'Error fetching data for {domain}: {response.status_code}')
                results[domain] = {'error': 'Data retrieval error'}

        return results

core_web_vitals_api = CoreWebVitalsAPI(api_key='AIzaSyAiwH_F1IXfGlOHUUP0qL0cKvm5SVLkuYg')

@app.route('/get_core_web_vitals', methods=['POST'])
def get_core_web_vitals_route():    
    data = request.get_json()
    domains = data.get('domains', [])
    if not domains:
        return jsonify({'error': 'Domains not provided'}), 400

    core_web_vitals_data = core_web_vitals_api.get_core_web_vitals(domains)
    return jsonify(core_web_vitals_data)

if __name__ == '__main__':
    app.run(debug=True)
