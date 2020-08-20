#!/usr/bin/env python
import ephem
from ephem import *
import pytz, datetime, time
from pytz import timezone
import json
import urllib.error
import urllib.parse
import urllib.request
from geopy.geocoders import Nominatim
from pyowm.owm import OWM
import os
from keys import Your_API_key

os.system("") # this is for print color text
print("\n")
# Get location information 
inp                         = input("Please enter city here (For example: London, Los Angeles, US):")
CityName                    = inp
utc                         = timezone('UTC')
CurrentUTCnDateTime         = datetime.datetime.utcnow()
geolocator                  = Nominatim(user_agent="Python")
location                    = geolocator.geocode(CityName)
lat_lng                     = (location.latitude, location.longitude)
TIMEZONE_BASE_URL           = "https://api.teleport.org/api/locations/" + str(lat_lng[0]) + ',' + str(lat_lng[1]) + "/?embed=location:nearest-cities/location:nearest-city/city:timezone"

try:
    # Get the API response.
    response                = urllib.request.urlopen(TIMEZONE_BASE_URL)

except urllib.error.URLError:
    pass  # Fall through to the retry loop.
else:
    # If we didn't get an IOError then parse the result.
    result                  = json.load(response)
    LocationTimezone        = result['_embedded']['location:nearest-cities'][0]['_embedded']['location:nearest-city']['_embedded']['city:timezone']['iana_name']

# for weather
owm                         = OWM(Your_API_key)  
weather_mgr                 = owm.weather_manager()
mgr                         = owm.weather_manager()
observation                 = mgr.weather_at_place(CityName)
weather                     = observation.weather           
temp                        = weather.temperature()         
wind_dict_in_meters_per_sec = observation.weather.wind()    
pressure_dict               = observation.weather.pressure  

# Observer settings for PyEphem
Viewpoint                   = ephem.Observer()
Viewpoint.pressure          = pressure_dict['press']             
Viewpoint.horizon           = '-0:34'                       
Viewpoint.temp              = temp["temp"]                 
Viewpoint.elevation         = 10                            
Viewpoint.lat               = str(lat_lng[0])               
Viewpoint.lon               = str(lat_lng[1])               

#Sunrise and sunset 
ViewpointSunrise            = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
ViewpointSet                = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

#Computing twilight
Viewpoint.horizon           = '-0:0'                        #
HorizonTwilightRising       = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
HorizonTwilightSetting      = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

Viewpoint.horizon           = '-6'                          # Civil Twilightn.
CivilTwilightRising         = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
CivilTwilightSetting        = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

Viewpoint.horizon           = '-12'                         # Nautical twilight.
NauticalTwilightRising      = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
NauticalTwilightSetting     = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

Viewpoint.horizon           = '-18'                         # Astronomical twilight.
AstronomicalTwilightRising  = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
AstronomicalTwilightSetting = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

#Golden hour (from -4° to 6°)
Viewpoint.horizon           = '6'                           # Astronomical twilight.
GoldenHighRising            = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
GoldenHighSetting           = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

Viewpoint.horizon           = '-4'                          # Astronomical twilight.
GoldenLowRising             = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
GoldenLowSetting            = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

#Blue hour (from -6° to -4°)
Viewpoint.horizon           = '-4'                          # Astronomical twilight.
BlueHighRising              = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
BlueHighSetting             = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

Viewpoint.horizon           = '-6'                          # Astronomical twilight.
BlueLowRising               = ephem.to_timezone(Viewpoint.next_rising(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
BlueLowSetting              = ephem.to_timezone(Viewpoint.next_setting(ephem.Sun()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

MoonRising                  = ephem.to_timezone(Viewpoint.next_rising(ephem.Moon()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))
MoonSetting                 = ephem.to_timezone(Viewpoint.next_setting(ephem.Moon()), ephem.UTC).replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone))

#Print data 数据打印
print((
    f"当地时区(Timezone):           {LocationTimezone}\n"                   #
    f"当地纬度(Latitude):           {Viewpoint.lat}\n"                      # 
    f"当地经度(Longitude):          {Viewpoint.lon}\n"                      #
    f'当地日期(Date):               {CurrentUTCnDateTime.replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone)).strftime("%Y-%m-%d")}\n'
    f'当地时间(Time):               {CurrentUTCnDateTime.replace(tzinfo=utc).astimezone(pytz.timezone(LocationTimezone)).strftime("%X -%Z")}\n'
    f'全天气象(Status):             {weather.status}\n'                                                 #
    f'详细气象(Details Status):     {weather.detailed_status}\n'                                        #
    f'当地气压(Pressure):           {pressure_dict["press"]} hPa\n'                                     #
    f'当地气温(Temperature):        {str(int(temp["temp"] -273.15))} °C\n'                              #
    f'最高温度(Max Temperature):    {str(int(temp["temp_max"] -273.15))} °C\n'                          #
    f'最低温度(Min Temperature):    {str(int(temp["temp_min"] -273.15))} °C\n'                          #
    f'当地风速(Wind Speed):         {str(int(wind_dict_in_meters_per_sec["speed"]*3.6))} km/h \n'       #
    f'当地风向(Wind Degree):        {str(int(wind_dict_in_meters_per_sec["deg"]))} °\n'                 #
    f'\n'
    f'当地日出(Sunrise)             \033[1;31m{ViewpointSunrise.strftime("%X -%Z")} 海军\033[0m\n'        
    f'天文曙暮光(AstronmyTwilight): 开始：{AstronomicalTwilightRising.strftime("%X -%Z")}, 结束: {HorizonTwilightRising.strftime("%X -%Z")} \n'
    f'航海曙暮光(NauticalTwilight): 开始：{NauticalTwilightRising.strftime("%X -%Z")}, 结束: {HorizonTwilightRising.strftime("%X -%Z")} \n'
    f'民用曙暮光(CivilTwilight):    开始: {CivilTwilightRising.strftime("%X -%Z")}, 结束: {HorizonTwilightRising.strftime("%X -%Z")} \n'
    f'蓝色时段(Blue Hour):          开始：{BlueLowRising.strftime("%X -%Z")}, 结束：{BlueHighRising.strftime("%X -%Z")}\n'
    f'金色时段(Golden Hour):        开始：{GoldenLowRising.strftime("%X -%Z")}, 结束：{GoldenHighRising.strftime("%X -%Z")}\n'
    f'当地日落(Sunset)              \033[1;31m{ViewpointSet.strftime("%X -%Z")} 海军\033[0m\n'
    f'金色时段(Golden Hour):        开始：{GoldenHighSetting.strftime("%X -%Z")}, 结束：{GoldenLowSetting.strftime("%X -%Z")}\n'
    f'蓝色时段(Blue Hour):          开始：{BlueHighSetting.strftime("%X -%Z")}, 结束：{BlueLowSetting.strftime("%X -%Z")}\n'
    f'民用曙暮光(CivilTwilight):    开始：{HorizonTwilightSetting.strftime("%X -%Z")}, 结束: {CivilTwilightSetting.strftime("%X -%Z")}\n'
    f'航海曙暮光(NauticalTwilight): 开始：{HorizonTwilightSetting.strftime("%X -%Z")}, 结束: {NauticalTwilightSetting.strftime("%X -%Z")}\n'
    f'天文曙暮光(AstronmyTwilight): 开始：{HorizonTwilightSetting.strftime("%X -%Z")}, 结束: {AstronomicalTwilightSetting.strftime("%X -%Z")}\n'
    f'\n'
    f'月亮时间(Moon):               出升：{MoonRising.strftime("%X -%Z")}, 落山：{MoonSetting.strftime("%X -%Z")}\n'
))

'