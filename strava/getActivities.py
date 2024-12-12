import requests

# Strava API-Endpunkt und Token
strava_url = 'https://www.strava.com/api/v3/athlete/activities'
strava_token = '3944493dc24639d8927ffab358c2805ea05519cc'

# OpenAI API-Endpunkt und Schlüssel
openai_url = 'https://api.openai.com/v1/completions'
openai_api_key = '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'

# Abrufen der Aktivitäten von Strava
response = requests.get(strava_url, headers={
                        'Authorization': f'Bearer {strava_token}'})
activities = response.json()

# Verarbeiten der Aktivitäten mit OpenAI
for activity in activities:
    prompt = f"Analysiere die folgende Aktivität: {activity['name']} mit {activity['distance']} Metern."
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 150
    }
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    openai_response = requests.post(openai_url, json=data, headers=headers)
    analysis = openai_response.json()
    print(analysis['choices'][0]['text'])
