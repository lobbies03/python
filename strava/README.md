curl -X POST https://www.strava.com/oauth/token \
-d client_id=140610 \
-d client_secret=a329b59bd7b634db79be5c012094094eb87ccab2 \
-d grant_type=refresh_token \
-d refresh_token=393c47541c73acfffdf3ff369b52cda0db9cd968



https://www.strava.com/oauth/authorize
?client_id=YOUR_CLIENT_ID
&redirect_uri=YOUR_REDIRECT_URI
&response_type=code
&scope=read,activity:read

https://www.strava.com/oauth/authorize
?client_id=140610
&redirect_uri=https://localhost:8181
&response_type=code
&scope=read,activity:read

