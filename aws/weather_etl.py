####
# weather_etl.py
# pull weather data, store in S3
# Conner Brown
# 4/18/2022
####

import os
import pandas as pd
import boto3
import datetime
today_str = datetime.datetime.today().strftime('%Y-%m-%d')

###################
### Weather API ###
###################
locations = {'Lawrence,KS':{'lat':38.9717,'long':95.2353},
             'San Diego,CA':{'lat':32.7157,'long':117.1611},
             'San Francisco,CA':{'lat':37.7749,'long':122.4194},
             'Burlington,VT':{'lat':44.4759,'long':73.2121}
            }


from pyowm.owm import OWM
api_key = 'f4e7944c907013d8457ae4c279527e88'

owm = OWM(api_key)
mgr = owm.weather_manager()

# df_weather.csv - actual weather by date, location
df_weather = pd.DataFrame(columns=['date','location','temperature'])
# df_forecasts.csv - forecasted weather by date, forecast_date, location
df_forecast = pd.DataFrame(columns=['date','location','forecast_date','temperature'])

for location in locations.keys():
    one_call = mgr.one_call(lat=locations[location]['lat'], lon=locations[location]['long'], units='imperial')
    # weather
    temp = one_call.current.temperature()
    print(location,temp)
    df_weather = df_weather.append({'date':today_str,
                                    'location':location,
                                    'temperature':temp
                                   },ignore_index=True)

    # forecasts
    forecasts = one_call.forecast_daily
    for forecast in forecasts:
        temp = forecast.temperature()['day']
        reference_time = forecast.reference_time()
        forecast_date = datetime.datetime.fromtimestamp(reference_time).strftime('%Y-%m-%d')
        df_forecast = df_forecast.append({'date':today_str,
                                          'forecast_date':forecast_date,
                                          'location':location,
                                          'temperature':temp
                                         },ignore_index=True)


#####################
### S3 Connection ###
#####################
from boto3.session import Session

### user01 - S3FullAccess
aws_access_key_id='AKIAQYHE4QT5OXO4QEMA'
aws_secret_access_key='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'

session = Session(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
s3 = session.resource('s3')
my_bucket = s3.Bucket('conner0and2-helloworld')


fname = "df_weather.csv"
# download data
my_bucket.download_file(Key=fname,Filename=fname)
if os.path.exists(fname):
    df = pd.read_csv(fname,index_col=0)
else:
    df = pd.DataFrame()
# append to df
df = df.append(df_weather,ignore_index=True)
# upload to S3
df.to_csv(fname)
my_bucket.upload_file(Filename=fname,Key=fname)


fname = "df_forecast.csv"
# download data
my_bucket.download_file(Key=fname,Filename=fname)
if os.path.exists(fname):
    df = pd.read_csv(fname,index_col=0)
else:
    df = pd.DataFrame()
# append to df
df = df.append(df_forecast,ignore_index=True)
# upload to S3
df.to_csv(fname)
my_bucket.upload_file(Filename=fname,Key=fname)

#############
### Email ###
#############
from botocore.exceptions import ClientError
SENDER = "conner0and2@gmail.com"
RECIPIENT = "conner0and2@gmail.com"
region_name = "us-west-1"
CHARSET = "UTF-8"

SUBJECT = "Weather ETL | "+today_str

message = "adding {} records to weather dataset \
adding {} records to forecast dataset".format(df_weather.shape[0],df_forecast.shape[0])
            
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Weather ETL Success</h1>
  <p>{message}</p>
</body>
</html>
            """            
BODY_HTML = BODY_HTML.format(message=message)
BODY_HTML.replace("{", "{{").replace("}", "}}")


# Create a new SES resource and specify a region.
# aws access user02: SESFullAccess
client = boto3.client('ses',region_name=region_name,aws_access_key_id = aws_access_key_id,aws_secret_access_key = aws_secret_access_key)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )
# Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])