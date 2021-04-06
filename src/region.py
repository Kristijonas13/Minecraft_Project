#Author: Kristijonas Bileisis
#Date Created: 04/06/2021
#Last Modified: 04/06/2021
#Description: Python file containing functions that inserts, updates, and deletes records from the region tables. 


#imports
import logging
import yaml
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
    print(insert_list)



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
            insert_list.append(region_file[:-4])
            for region in region_list:
                if str(region[0]) == str(region_file[:-4]):
                    insert_list.remove(region[0])
        return insert_list

    except sqlite3.Error as error:
        print("error")



def check_delete(cursor):
    print("check")



def check_update(region_path, cursor):

    try: 
        update_list = []
        filename_list = check_last_modified(region_path, cursor)

        for filename in filename_list: 
            file = open(filename, 'r')
            list = yaml.load(file, Loader=yaml.FullLoader)
            

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