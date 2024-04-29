from tests import *

from crime_project import *
import matplotlib.pyplot as plt


def plot_crime_hotspot():
    conn = connect_db()
    result = get_crime_hotspot(conn)
    result.show()


def do_plots():
    conn = connect_db()
    plot_victim_age_dist(conn)

    #Creating a subplot of 2x2 grid
    _fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(20, 10))

    conn = connect_db()
    plot_crime_occurance_over_time(conn, axis=axes[0][0])

    conn = connect_db()
    plot_crimes_based_on_current_status(conn, axis=axes[0][1])
   
    conn = connect_db()
    plot_location_of_crime(conn, axis=axes[1][0])

   

    # Creating a subplot of 2x1 grid
    _fig1, axes1 = plt.subplots(nrows=2, ncols=1,figsize=(15,8))

    conn = connect_db()
    plot_reported_crime(conn, axis1=axes1[0])

    conn = connect_db()
    plot_victim_premis_distribution(conn, axis1=axes1[1])

    plot_crime_hotspot()
    plt.show()


    #Printing the records on the console
def print_total_records():
    #Prints the Total Number of records
    conn = connect_db()
    result = get_total_records(conn)
    print('\nTotal number of records : ', next(iter(result)))


def print_unique_crime_codes():
    #Prints Unique Crime codes and their description
    conn = connect_db()
    df = get_unique_crime_codes(conn)
    print('\n\nUnique crime codes and their description\n', df)


def print_unique_values_of(col_name):
    #Prints the Number of Unique Values
    conn = connect_db()

    result = get_unique_values_of(conn, col_name)
    print(f'\n\nUnique values in {col_name} column is :', len(result))





if __name__ == '__main__':
    
    print_total_records()
    print_unique_crime_codes()
    print_unique_values_of(col_name='PREMIS_DESC')

    
    do_plots()
