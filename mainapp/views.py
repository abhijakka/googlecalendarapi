from django.shortcuts import render,redirect

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        'client_secret_927819335396-3ea4tk8a4uoiemmbgft57iudla7r151l.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/'
        )
   
            
            
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    a=request.session['state'] = state
    print(a,authorization_url,'gchhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    
    return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    state = request.session['state']
   

    print(state)
    flow = Flow.from_client_secrets_file(
        'client_secret_927819335396-3ea4tk8a4uoiemmbgft57iudla7r151l.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/',
        state=state,
        
       
        
       )

    # authorization_response = request.build_absolute_uri()
    authorization_response = request.build_absolute_uri()
    if "http:" in authorization_response:
        authorization_response = "https:" + authorization_response[5:]
        print(authorization_response)
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    return render(request, 'calendar.html', {'events': events})
