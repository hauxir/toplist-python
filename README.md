# toplist-python
Python wrapper to talk to the Toplist API http://thetoplistapp.com

# Installation
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Usage
1. Login at:

https://www.facebook.com/v2.8/dialog/oauth?redirect_uri=fb1832655376972820%3A%2F%2Fauthorize%2F&state=%7B%22challenge%22%3A%22TmhoovL4TZtEJduJuxfewrMtUlU%253D%22%2C%220_auth_logger_id%22%3A%22AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=public_profile%2Cemail&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=1832655376972820&ret=login&sdk=ios&fbapp_pres=1&logger_id=AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7&ext=1494637564&hash=AeYAq8B7CAB7h3SZ

2. Look at the response in https://www.facebook.com/v2.8/dialog/oauth/confirm?dpr=2 and find the token
3. Pass that token to login the toplist module
