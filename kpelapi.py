
import pandas as pd
import requests
import json
from pandas.io.json import json_normalize
from functools import reduce


user = input('Enter your username or email: ')
pw = input('Enter your password: ')
excel = input('Specify Excel filename & location: ')

#Authenticate the user
s = requests.Session()
payload = {'username_or_email': user, 'password':pw}
s.post('https://api.onepeloton.com/auth/login', json=payload)


#Get User ID to pass into other calls
me_url = 'https://api.onepeloton.com/api/me'
response = s.get(me_url)
apidata = s.get(me_url).json()

#Flatten API response into a temporary dataframe
df_my_id = json_normalize(apidata, 'id', ['id']) 
df_my_id_clean = df_my_id.iloc[0]
my_id = (df_my_id_clean.drop([0])).values.tolist()