#Creator: Kristijonas Bileisis
#Date Created: 3/15/2021
#Last Modified: 3/15/2021
#Description: Python file containing functions that deal with deleting no longer existing players or records from the database. 

#function that goes through and checks and deletes records from the database
#returns false if an error occurs
def delete_records():


#compare database and minecraft server to see which players no longer exist
#returns list of playerID's that no longer exist on the server
def check_if_player_exists():

#takes in a list of playerID's and deletes those records from the player_info table, reputation_points table, & legendary_beasts_killed table
# returns true/false based on if the user was deleted or not
def delete_player_info():


#compare database and minecraft server to see which mobs no longer exist
#returns list of mob_names that no longer exist on the server
def check_if_mob_exists():

#takes in a list of mob_names and deletes those records from the mob_info table & drops_info table. 
#returns true/false based on if the mob was deleted successfully or not
def delete_mob_info():


#compare database and minecraft server to see which legendary_beasts no longer exist
#returns list of legendary_beast_names that no longer exist on the server
def check_if_legendary_beast_exists():

#takes in a list of legendary_beast_names and deletes those records from the legendary_beasts info table & drops_info table.
#returns true/false based on if the legendary_beast was deleted successfully or not
def delete_legendary_beast_info():


#compare database and minecraft server to see which locations no longer exist
#returns list of locationID's that no longer exist on the server
def check_if_location_exists():

# takes in a list of locationID's and deletes those records from the location_info table
# returns true/false based on if the location was deleted successfully or not
def delete_location_info():
