import requests
import json

# Replace with your Qlik SaaS tenant URL and API key
tenant_url = 'https://m3data.eu.qlikcloud.com'
api_key = 'eyJhbGciOiJFUzM4NCIsImtpZCI6IjQ3MDNhMDc4LTBjMTgtNGQ2My04M2ZiLWFlMTgxNjI2ODQ3NyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiaGlNd1lsZEZFd3dGZzRMYnJ1Y2pVcHVCVU5CbG5BMnIiLCJqdGkiOiI0NzAzYTA3OC0wYzE4LTRkNjMtODNmYi1hZTE4MTYyNjg0NzciLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNGphX3VPUl9UN185elpLSzJwOFRtdUZKdTBkeXZBclIifQ.yfZOlKVbcRbj6VmJIVoonY2aJVkaQ_Kt4KSISvwpRo3NjKHrNInP0rh7umThrhA3giw6A8BmWjv3DzcOvRyBTo2ApHBsQFROegMwmDw4YIl7wxq53OwmTv3QQM2kDuJV'

# Function to get the app ID by app name
def get_app_id(app_name):
    url = f'{tenant_url}/api/v1/apps'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    apps = response.json()  # Parse the JSON response
    
    for app in apps['data']:
        if app['attributes']['name'] == app_name:  # Match the app name
            return app['attributes']['id']
    return None  # Return None if app not found

# Function to export the app and get the download path
def export_app(app_id):
    url = f'{tenant_url}/api/v1/apps/{app_id}/export'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    response.raise_for_status()  # Ensure the request was successful
    return response.json()['downloadPath']  # Extract the download path

# Function to download the exported app using the download path
def download_app(download_path, output_file):
    url = f'{tenant_url}{download_path}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    
    with open(output_file, 'wb') as file:  # Write the content to a file
        file.write(response.content)

# Main script
app_name = 'Data Diagnostics-Profilehist-20240514'
output_file = 'myapp.qvf'

# Step 1: Get the app ID
app_id = get_app_id(app_name)
if not app_id:
    raise Exception(f'App named "{app_name}" not found')

# Step 2: Export the app and get the download path
download_path = export_app(app_id)

# Step 3: Download the exported app using the download path
download_app(download_path, output_file)

print(f'App "{app_name}" has been exported to {output_file}')
