import boto3
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from collections import Counter
import os
import urllib.parse

app = Flask(__name__)

def get_cloudtrail_events(start_time, end_time, aws_credentials):
    session = boto3.Session(
        aws_access_key_id=aws_credentials['aws_access_key_id'],
        aws_secret_access_key=aws_credentials['aws_secret_access_key'],
        region_name=aws_credentials['aws_region']
    )
    cloudtrail = session.client('cloudtrail')
    
    params = {
        'StartTime': start_time,
        'EndTime': end_time,
        'LookupAttributes': [
            {
                'AttributeKey': 'ReadOnly',
                'AttributeValue': 'false'
            },
        ]
    }
    
    events = []
    
    while True:
        response = cloudtrail.lookup_events(**params)
        events.extend(response['Events'])
        
        if 'NextToken' not in response:
            break
        params['NextToken'] = response['NextToken']
    
    return events

def get_username(event):
    # Tenta obter o username de diferentes campos possíveis
    if 'Username' in event:
        return event['Username']
    elif 'userIdentity' in event and 'userName' in event['userIdentity']:
        return event['userIdentity']['userName']
    elif 'userIdentity' in event and 'principalId' in event['userIdentity']:
        return event['userIdentity']['principalId']
    else:
        return 'Unknown User'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_logs', methods=['POST'])
def get_logs():
    data = request.json
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])
    
    aws_credentials = {
        'aws_access_key_id': data['aws_access_key_id'],
        'aws_secret_access_key': data['aws_secret_access_key'],
        'aws_region': data['aws_region']
    }
    
    try:
        events = get_cloudtrail_events(start_time, end_time, aws_credentials)
        
        event_counts = Counter(event['EventName'] for event in events)
        user_counts = Counter(get_username(event) for event in events)
        
        result = {
            'event_counts': dict(event_counts),
            'user_counts': dict(user_counts)
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event_details/<event_name>')
def event_details(event_name):
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return redirect(url_for('index'))
    
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    
    aws_credentials = {
        'aws_access_key_id': request.args.get('aws_access_key_id'),
        'aws_secret_access_key': request.args.get('aws_secret_access_key'),
        'aws_region': request.args.get('aws_region')
    }
    
    try:
        events = get_cloudtrail_events(start_time, end_time, aws_credentials)
        filtered_events = [event for event in events if event['EventName'] == event_name]
        
        for event in filtered_events:
            if 'CloudTrailEvent' in event:
                try:
                    cloud_trail_event = json.loads(event['CloudTrailEvent'])
                    event['CloudTrailEvent'] = json.dumps(cloud_trail_event, indent=2)
                except json.JSONDecodeError:
                    pass
            event['Username'] = get_username(event)
        
        return render_template('event_details.html', 
                               event_name=event_name, 
                               events=filtered_events, 
                               start_time=start_time.isoformat(),
                               end_time=end_time.isoformat(),
                               aws_credentials=aws_credentials)
    except Exception as e:
        return f"Error: {str(e)}", 400

@app.route('/user_details/<username>')
def user_details(username):
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return redirect(url_for('index'))
    
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    
    aws_credentials = {
        'aws_access_key_id': request.args.get('aws_access_key_id'),
        'aws_secret_access_key': request.args.get('aws_secret_access_key'),
        'aws_region': request.args.get('aws_region')
    }
    
    try:
        events = get_cloudtrail_events(start_time, end_time, aws_credentials)
        filtered_events = [event for event in events if get_username(event) == username]
        
        for event in filtered_events:
            if 'CloudTrailEvent' in event:
                try:
                    cloud_trail_event = json.loads(event['CloudTrailEvent'])
                    event['CloudTrailEvent'] = json.dumps(cloud_trail_event, indent=2)
                except json.JSONDecodeError:
                    pass
            event['Username'] = get_username(event)
        
        return render_template('user_details.html', 
                               username=username, 
                               events=filtered_events, 
                               start_time=start_time.isoformat(),
                               end_time=end_time.isoformat(),
                               aws_credentials=aws_credentials)
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)