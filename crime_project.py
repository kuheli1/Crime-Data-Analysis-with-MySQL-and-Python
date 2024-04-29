
import pymysql
import seaborn as sns
import pandas as pd
import plotly.express as px


def connect_db():
    #Connect to MySQL DB
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='crime'
    )
    return conn
 

def get_total_records(conn):
    #3.Get the total records from the Crime Database
    with conn:
        with conn.cursor() as cursor:
            Total_Count = 'select count(Crm_Cd) as Total_Count from crime_data'
            cursor.execute(Total_Count)
            result = cursor.fetchone()
            return result


def get_unique_crime_codes(conn):
    #3.Get the distinct crime code and their description
    with conn:
        with conn.cursor() as cursor:
            # Read a single record
            sql = 'select DISTINCT Crm_Cd as Crime_Code, Crm_Cd_Desc as Crime_Desc from crime_data'
            cursor.execute(sql)
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=['Crime_Code', 'Crime_Description'])
            return df


def get_unique_values_of(conn, col):
    #3.Get the unique values in Specific Column, tested with Area Name column
    with conn:
        with conn.cursor() as cursor:
            unique = f'select DISTINCT {col} from crime_data'
            cursor.execute(unique)
            result = cursor.fetchall()
            return list(map(lambda x: x[0], result))


def plot_crime_occurance_over_time(conn,axis = None):
    #4.Determine trends in crime occurrence over time
    with conn:
        with conn.cursor() as cursor:
            crime = 'Select count(Crm_Cd),DATE_OCC from crime_data group by DATE_OCC'
            cursor.execute(crime)
            crime_result = cursor.fetchall()
            df = pd.DataFrame(crime_result,columns=['value','date'])
            sns.lineplot(data = df,x='date',y='value',ax=axis)
            axis.set_xlabel("Date")
            axis.set_ylabel("Crimes")
            axis.set_title("Crime occurance over time")
            axis.tick_params(labelrotation=90, labelsize=6)


def get_crime_hotspot(conn):
    '''5.Visualize crime hotspots on a map using Latitude and longitude
        Q - Where are the geographical hotspots for reported crimes?'''
    with conn:
        with conn.cursor() as cursor:
            hotspot = 'select LAT,LON from crime_data'
            cursor.execute(hotspot)
            crime_result = cursor.fetchall()
            df=pd.DataFrame(crime_result,columns =['lat','lon'])
            # sns.scatterplot(df,x='lat',y='lon',ax=axis)
            return px.density_mapbox(df, lat='lat', lon='lon', zoom=9, center={
                                        'lat': 34.05, 'lon': -118.3}, radius=50, mapbox_style='open-street-map')


def plot_victim_age_dist(conn, axis = None):
    '''6.distribution of victim ages and genders
        Q:What is the distribution of victim ages in reported crimes?
        Q:Is there a significant difference in crime rates between male and female victims?'''
    with conn:
        with conn.cursor() as cursor:
            vict = "select Vict_Age,Vict_Sex from crime_data group by 1,2 having Vict_Sex != ''"
            cursor.execute(vict)
            vict_result = cursor.fetchall()
            df=pd.DataFrame(vict_result,columns=['Age','Gender'])
            sns.displot(df, x="Age", hue="Gender", multiple="dodge")


def plot_victim_premis_distribution(conn, axis1=None):
    #6.premises descriptions where crimes occur.
    with conn:
        with conn.cursor() as cursor:
            vict = 'select Premis_Desc, Vict_Age, Vict_Sex from crime_data group by 1, 2, 3 order by 1'
            cursor.execute(vict)
            vict_result = cursor.fetchall()
            result=pd.DataFrame(vict_result,columns=['Premis','Age','Gender'])
            sns.scatterplot(result, x="Premis", y="Age", hue="Gender", ax=axis1)
            axis1.tick_params(labelrotation=90, labelsize=6)
            axis1.set_title("Premise Description where crimes occur")


def plot_location_of_crime(conn, axis=None):
    '''Crimes based on location
        Q.Where do most crimes occur based on the "Location" column?'''
    with conn:
        with conn.cursor() as cursor:
            # loc = 'select Location, from crime_data'
            loc = 'select Location,count(Location) from crime_data group by 1 order by 2 desc limit 20;'
            cursor.execute(loc)
            result = cursor.fetchall()
            crime_location = pd.DataFrame(result,columns=['Location','Count'])
            sns.barplot(crime_location, x="Count", y="Location", ax=axis)
            axis.set_xlabel("Crime Count")
            axis.set_title("Top Locations with Crime")


def plot_crimes_based_on_current_status(conn, axis=None):
    #7.crimes based on their current status
    with conn:
        with conn.cursor() as cursor:
            stat = 'select Status from crime_data'
            cursor.execute(stat)
            stat_result = cursor.fetchall()
            stat_res = {'Status': []}
            for i in stat_result:
                status = i[0]
                stat_res['Status'].append(status)
            sns.countplot(stat_res,x='Status',ax=axis)
            

    
def plot_reported_crime(conn,axis1=None):
    #Q:What is the distribution of reported crimes based on Crime Code?
    with conn:
        with conn.cursor() as cursor:
            code = 'select Crm_Cd from crime_data group by 1'
            cursor.execute(code)
            crime_code = cursor.fetchall()
            df = pd.DataFrame(crime_code,columns=['crime_code'])
            sns.histplot(df,x='crime_code',ax=axis1)
            axis1.set_xlabel("CrimeCode")



