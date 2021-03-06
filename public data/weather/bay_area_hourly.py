import pandas as pd
import numpy as np
import time
import keyring
import datetime
import requests


bay_area_cities = ["Alameda",#	City	Alameda	73,812	10.61	27.5	April 19, 1854
"Albany",#	City	Alameda	18,539	1.79	4.6	September 22, 1908
"American",# Canyon	City	Napa	19,454	4.84	12.5	January 1, 1992
"Antioch",#	City	Contra Costa	102,372	28.35	73.4	February 6, 1872
"Atherton",#	Town	San Mateo	6,914	5.02	13.0	September 12, 1923
"Belmont",#	City	San Mateo	25,835	4.62	12.0	October 29, 1926
"Belvedere",#	City	Marin	2,068	0.52	1.3	December 24, 1896
"Benicia",#	City	Solano	26,997	12.93	33.5	March 27, 1850
"Berkeley",#	City	Alameda	112,580	10.47	27.1	April 4, 1878
"Brentwood",#	City	Contra Costa	51,481	14.79	38.3	January 21, 1948
"Brisbane",#	City	San Mateo	4,282	3.10	8.0	November 27, 1961
"Burlingame",#	City	San Mateo	28,806	4.41	11.4	June 6, 1908
"Calistoga",#	City	Napa	5,155	2.60	6.7	January 6, 1886
"Campbell",#	City	Santa Clara	39,349	5.80	15.0	March 28, 1952
"Clayton",#	City	Contra Costa	10,897	3.84	9.9	March 18, 1964
"Cloverdale",#	City	Sonoma	8,618	2.65	6.9	February 28, 1872
"Colma",#	Town	San Mateo	1,792	1.91	4.9	August 5, 1924
"Concord",#	City	Contra Costa	122,067	30.55	79.1	February 9, 1905
"Corte Madera",#	Town	Marin	9,253	3.16	8.2	June 10, 1916
"Cotati",#	City	Sonoma	7,265	1.88	4.9	July 16, 1963
"Cupertino",#	City	Santa Clara	58,302	11.26	29.2	October 10, 1955
"Daly City",#	City	San Mateo	101,123	7.66	19.8	March 22, 1911
"Danville",#	Town	Contra Costa	42,039	18.03	46.7	July 1, 1982
"Dixon",#	City	Solano	18,351	7.00	18.1	March 30, 1878
"Dublin",#	City	Alameda	46,036	14.91	38.6	February 1, 1982
"East Palo Alto",#	City	San Mateo	28,155	2.51	6.5	July 1, 1983
"El Cerrito",#	City	Contra Costa	23,549	3.69	9.6	August 23, 1917
"Emeryville",#	City	Alameda	10,080	1.25	3.2	December 8, 1896
"Fairfax",#	Town	Marin	7,441	2.20	5.7	March 2, 1931
"Fairfield",#County seat	City	Solano	105,321	37.39	96.8	December 12, 1903
"Foster City",#	City	San Mateo	30,567	3.76	9.7	April 27, 1971
"Fremont",#	City	Alameda	214,089	77.46	200.6	January 23, 1956
"Gilroy",#	City	Santa Clara	48,821	16.15	41.8	March 12, 1870
"Half Moon Bay",#	City	San Mateo	11,324	6.42	16.6	July 15, 1959
"Hayward",#	City	Alameda	144,186	45.32	117.4	March 11, 1876
"Healdsburg",#	City	Sonoma	11,254	4.46	11.6	February 20, 1867
"Hercules",#	City	Contra Costa	24,060	6.21	16.1	December 15, 1900
"Hillsborough",#	Town	San Mateo	10,825	6.19	16.0	May 5, 1910
"Lafayette",#	City	Contra Costa	23,893	15.22	39.4	July 29, 1968
"Larkspur",#	City	Marin	11,926	3.03	7.8	March 1, 1908
"Livermore",#	City	Alameda	80,968	25.17	65.2	April 1, 1876
"Los Altos",#	City	Santa Clara	28,976	6.49	16.8	December 1, 1952
"Los Altos Hills",#	Town	Santa Clara	7,922	8.80	22.8	January 27, 1956
"Los Gatos",#	Town	Santa Clara	29,413	11.08	28.7	August 10, 1887
"Martinez",#County seat	City	Contra Costa	35,824	12.13	31.4	April 1, 1876
"Menlo Park",#	City	San Mateo	32,026	9.79	25.4	November 23, 1927
"Mill Valley",#	City	Marin	13,903	4.76	12.3	September 1, 1900
"Millbrae",#	City	San Mateo	21,532	3.25	8.4	January 14, 1948
"Milpitas",#	City	Santa Clara	66,790	13.59	35.2	January 26, 1954
"Monte Sereno",#	City	Santa Clara	3,341	1.62	4.2	May 14, 1957
"Moraga",#	Town	Contra Costa	16,016	9.43	24.4	November 13, 1974
"Morgan Hill",#	City	Santa Clara	37,882	12.88	33.4	November 10, 1906
"Mountain View",#	City	Santa Clara	74,066	12.00	31.1	November 7, 1902
"Napa",#County seat	City	Napa	76,915	17.84	46.2	March 23, 1872
"Newark",#	City	Alameda	42,573	13.87	35.9	September 22, 1955
"Novato",#	City	Marin	51,904	27.44	71.1	January 20, 1960
"Oakland",#County seat	City	Alameda	390,724	55.79	144.5	May 4, 1852
"Oakley",#	City	Contra Costa	35,432	15.85	41.1	July 1, 1999
"Orinda",#	City	Contra Costa	17,643	12.68	32.8	July 1, 1985
"Pacifica",#	City	San Mateo	37,234	12.66	32.8	November 22, 1957
"Palo Alto",#	City	Santa Clara	64,403	23.88	61.8	April 23, 1894
"Petaluma",#	City	Sonoma	57,941	14.38	37.2	April 12, 1858
"Piedmont",#	City	Alameda	10,667	1.68	4.4	January 31, 1907
"Pinole",#	City	Contra Costa	18,390	5.32	13.8	June 25, 1903
"Pittsburg",#	City	Contra Costa	63,264	17.22	44.6	June 25, 1903
"Pleasant Hill",#	City	Contra Costa	33,152	7.07	18.3	November 14, 1961
"Pleasanton",#	City	Alameda	70,285	24.11	62.4	June 18, 1894
"Portola Valley",#	Town	San Mateo	4,353	9.09	23.5	July 14, 1964
"Redwood City",#County seat	City	San Mateo	76,815	19.42	50.3	May 11, 1867
"Richmond",#	City	Contra Costa	103,701	30.07	77.9	August 7, 1905
"Rio Vista",#	City	Solano	7,360	6.69	17.3	January 6, 1894
"Rohnert Park",#	City	Sonoma	40,971	7.00	18.1	August 28, 1962
"Ross",#	Town	Marin	2,415	1.56	4.0	August 21, 1908
"St. Helena",#	City	Napa	5,814	4.99	12.9	March 24, 1876
"San Anselmo",#	Town	Marin	12,336	2.68	6.9	April 9, 1907
"San Bruno",#	City	San Mateo	41,114	5.48	14.2	December 23, 1914
"San Carlos",#	City	San Mateo	28,406	5.54	14.3	July 8, 1925
"San Francisco",#County seat	City and county	San Francisco	805,235	46.87	121.4	April 16, 1850[10]
"San Jose",#County seat	City	Santa Clara	1,023,827	176.53	457.2	March 27, 1850
"San Leandro",#	City	Alameda	84,950	13.34	34.6	March 21, 1872
"San Mateo",#	City	San Mateo	97,207	12.13	31.4	September 4, 1894
"San Pablo",#	City	Contra Costa	29,139	2.63	6.8	April 27, 1948
"San Rafael",#County seat	City	Marin	57,713	16.47	42.7	February 18, 1874
"San Ramon",#	City	Contra Costa	72,148	18.06	46.8	July 1, 1983
"Santa Clara",#	City	Santa Clara	116,468	18.41	47.7	July 5, 1852
"Santa Rosa",#County seat	City	Sonoma	177,586	41.50	107.5	March 26, 1868
"Saratoga",#	City	Santa Clara	29,926	12.38	32.1	October 22, 1956
"Sausalito",#	City	Marin	7,061	1.77	4.6	September 4, 1893
"Sebastopol",#	City	Sonoma	7,379	1.85	4.8	June 13, 1902
"Sonoma",#	City	Sonoma	10,648	2.74	7.1	September 3, 1883
"South San Francisco",#	City	San Mateo	63,632	9.14	23.7	September 19, 1908
"Suisun City",#	City	Solano	28,111	4.11	10.6	October 9, 1868
"Sunnyvale",#	City	Santa Clara	140,081	21.99	57.0	December 24, 1912
"Tiburon",#	Town	Marin	8,962	4.43	11.5	June 23, 1964
"Union City",#	City	Alameda	69,516	19.47	50.4	January 26, 1959
"Vacaville",#	City	Solano	92,428	28.37	73.5	August 9, 1892
"Vallejo	City",#	Solano	115,942	30.67	79.4	March 30, 1868
"Walnut Creek",#	City	Contra Costa	64,173	19.76	51.2	October 21, 1914
"Windsor",#	Town	Sonoma	26,801	7.27	18.8	July 1, 1992
"Woodside",#	Town	San Mateo	5,287	11.73	30.4	November 16, 1956
"Yountville"]




df = pd.DataFrame()
s = pd.Series()
ap_base_url = "http://api.openweathermap.org/data/2.5/air_pollution?"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# 60 caslls per minute
sleep = np.ceil(len(bay_area_cities)/60)
for city in bay_area_cities[:5]:
    # 60 caslls per minute
    time.sleep(sleep)
    complete_url = base_url + "appid=" + keyring.get_password('owm','connerbrown') + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    if x['cod'] =="404":
        continue
    s['city'] = city
    s['lat'] = x['coord']['lat']
    s['lon'] = x['coord']['lon']
    s['weather_id'] = x['weather'][0]['id']
    s['weather_main'] = x['weather'][0]['main']
    s['weather_description'] = x['weather'][0]['description']
    s['weather_icon'] = x['weather'][0]['icon']
    s['temp'] = x['main']['temp']
    s['feels_like'] = x['main']['feels_like']
    s['temp_min'] = x['main']['temp_min']
    s['temp_max'] = x['main']['temp_max']
    s['pressure'] = x['main']['pressure']
    s['humidity'] = x['main']['humidity']
    s['visibility'] = x['visibility']
    s['wind_speed'] = x['wind']['speed']
    s['wind_deg'] = x['wind']['deg']
    #s['wind_gust'] = x['wind']['gust']
    s['clouds_all'] = x['clouds']['all']
    s['dt'] = x['dt']
    s['sunrise'] = x['sys']['sunrise']
    s['sunset'] = x['sys']['sunset']
    
    ## air pollution
    ap_complete_url = ap_base_url + "lat=" + str((s['lat'])) + "&lon=" + str((s['lon'])) + "&appid=" + keyring.get_password('owm','connerbrown')
    response = requests.get(ap_complete_url)
    y = response.json()
    s['aqi'] = y['list'][0]['main']['aqi']
    s['components_co'] = y['list'][0]['components']['co']
    s['components_no'] = y['list'][0]['components']['no']
    s['components_no2'] = y['list'][0]['components']['no2']
    s['components_o3'] = y['list'][0]['components']['o3']
    s['components_so2'] = y['list'][0]['components']['so2']
    s['components_pm2_5'] = y['list'][0]['components']['pm2_5']
    s['components_pm10'] = y['list'][0]['components']['pm10']
    s['components_nh3'] = y['list'][0]['components']['nh3']
    df = df.append(s,ignore_index=True)
df['dt_pt'] = pd.to_datetime(datetime.datetime.now())

pwd = "/Users/connerbrown/Documents/Github/dslab/public data/weather/"
df_full = pd.read_csv(pwd+'bay_area_hourly.csv',index_col=0)

df_full = df_full.append(df,ignore_index=True)
df_full.to_csv(pwd+'bay_area_hourly.csv')