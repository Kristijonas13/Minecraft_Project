#Author: Kristijonas Bileisis
#Date Created: 04/06/2021
#Last Modified: 04/06/2021
#Description: Python file containing functions that inserts, updates, and deletes records from the region tables. 


#imports
import logging
import json
import os 
import sqlite3
from datetime import datetime


def region(region_path, cursor):

    try: 
        check = check_region(region_path, cursor)

        if check[0]:
            delete_region(check[0], cursor)
        else: logging.info("No deletions to be made from region")

        if check[1]:
            insert_region(check[1], cursor, region_path)
        else: logging.info("No inserts to be made into region")

        if check[2]:
            update_region(check[2], cursor)
        else: logging.info("No updates to be made to region")

    except sqlite3.Error as error:
        logging.error("Sqlite Failed: ", error)    



def check_region(region_path, cursor):

    try: 
        delete_list = check_delete(cursor)
        insert_list = check_insert(region_path, cursor)
        update_list = check_update(region_path, cursor)

        return [delete_list, insert_list, update_list]
    except sqlite3.Error as error:
        logging.error("Sqlite Failed: ", error)



def delete_region(delete_list, cursor):

    try: 
        sqlite_delete_query = "delete from region where region_name in ('"
        
        for data in delete_list:
            logging.info("Deleting region name from region: %s", data[0])
            sqlite_delete_query = sqlite_delete_query + str(data[0] + "','")

        sqlite_delete_query = sqlite_delete_query[:-3] + "');"
        cursor.execute(sqlite_delete_query)

    except sqlite3.Error as error:
        logging.error("Failed to delete from region", error)



def insert_region(insert_list, cursor, region_path):

    data_list = [] 
    try: 
        for file_path in insert_list:
            with open(file_path) as file:
                region_dict = json.load(file)

        for table, columns in region_dict.items(): 
            print(table)
            for column in columns:
                print(column)
        ax = create_insert_query_list(['region_info', ['region_name', 'description']],region_dict)
        query_list = create_insert_queries(ax)
        for query in query_list: 
            cursor.execute(query)
        
    except sqlite3.Error as error:
        print("error")



def create_insert_queries(insert_query_list):

    queries = []
    
    for value in insert_query_list[2]:
        sqlite_insert_query = 'insert into ' + str(insert_query_list[0]) + ' ('
        for column_name in insert_query_list[1]:
            sqlite_insert_query = sqlite_insert_query + str(column_name) + ', '
        sqlite_insert_query= sqlite_insert_query[:-2] + ') values ('
        for valu in value: 
            sqlite_insert_query= sqlite_insert_query + "'"+str(valu) + "',"
        sqlite_insert_query = sqlite_insert_query[:-1] + ');' 
        queries.append(sqlite_insert_query)
    return queries
    
    


def create_insert_query_list(name_column,region_dict):

    insert_query_list = []
    ax = []
    ax.append(name_column[0])
    ax.append(name_column[1])
    ax.append(get_insert_values(region_dict[name_column[0]], name_column[1]))
    ax.append(len(name_column[1]))
    return ax

    #[region_table, [column1,column2], [(values),(value)], num_of_columns]

    
    values_list = get_insert_values

def get_insert_values(table_name, column_names_list):
    
    values_list = []
    values2_list = []
    for name in table_name:
        for column in column_names_list:
            values_list.append(name[column])
        values2_list.append(tuple(values_list))
        values_list = []
    return values2_list

#return nested list [region_name, last_modified, filename, table_to_modify, [[old_values,new_values]],]
def update_region(update_list, cursor):
    print("update")




def check_insert(region_path, cursor):
    insert_list = []

    try: 
        region_dir = os.listdir(region_path)
        sqlite_select_query = 'select region_name from region_info;'
        cursor.execute(sqlite_select_query)
        region_list = cursor.fetchall()

        for region_file in region_dir:
            region_file_path = str(region_path) + "\\" + str(region_file)
            insert_list.append(region_file_path)
            for region in region_list:
                if str(region[0]) == str(region_file[:-4]):
                    insert_list.remove(region_file_path)
        return insert_list

    except sqlite3.Error as error:
        print("error")



def check_delete(cursor):
    return []



def check_update(region_path, cursor):

    try: 
        update_list = []
        filename_list = check_last_modified(region_path, cursor)

    except sqlite3.Error as error:
        print("error")
    
    

def check_last_modified(region_path, cursor):

    region_list = []

    try: 
        region_dir = os.listdir(region_path)
        sqlite_select_query = 'select region_name, last_modified from region_info;'
        cursor.execute(sqlite_select_query)
        new_lm_list = cursor.fetchall()

        for region_file in region_dir:
            region_file_path = str(region_path) + "\\" + str(region_file)
            old_lm = get_last_modified(str(region_file_path))
            for new_lm in new_lm_list:
                if new_lm[0] == str(region_file[:-4]):
                    if str(new_lm[1]) != str(old_lm): 
                        region_list.append(region_file_path)

        return region_list

    except sqlite3.Error as error:
        print("error")


def get_last_modified(region_file):

    unix_created_time = os.path.getmtime(region_file)
    date_time = datetime.fromtimestamp(unix_created_time)
    return date_time  