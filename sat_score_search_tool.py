import numpy as np
import pandas as pd
import datetime
import urllib


# source data: https://data.cityofnewyork.us/Education/SAT-Results/f9bf-2cp4
query = ("https://data.cityofnewyork.us/resource/734v-jeq5.json?")
raw_data = pd.read_json(query)


# removes all of the rows where no test takes produced a value of 's' in the score columns which prevented my from changing the column type to int
raw_data_no_s = raw_data[raw_data.num_of_sat_test_takers != 's']  


# these change the datatype in all of the score columns to int so that I can run calculations off of them  
raw_data_no_s['sat_math_avg_score'] = raw_data_no_s['sat_math_avg_score'].astype(int)
raw_data_no_s['sat_critical_reading_avg_score'] = raw_data_no_s['sat_critical_reading_avg_score'].astype(int)
raw_data_no_s['sat_writing_avg_score'] = raw_data_no_s['sat_writing_avg_score'].astype(int)


# creates a new column in the dataframe and then populate it with the average of the three sat scores
raw_data_no_s['overall_average_score'] = (raw_data_no_s.sat_writing_avg_score + raw_data_no_s.sat_critical_reading_avg_score + raw_data_no_s.sat_math_avg_score) / 3


# user input prompted to indicate which score they want to sort by, if they want highest or lowest scoring schools, and how many to show
# added in print lines in attmpt to make the input prompts easier to see
print ""
search_target = raw_input("What specific sat score are you looking to rank schools by? (math, writing, critical reading, overall) ")
print ""
search_type = raw_input("Are you looking for the best schools or the worst? ")
print ""
search_size = raw_input("How long a list do you need? ")

# NEED - create a function that tests search_size input to make sure its just a number

# NEED - need to figure out how to fix the error message that python is returning when i run the program

# a function that prints list of schools based on user input search parameters
def search_function(s_type, s_target):
  
  stop_trigger_1 = True
  stop_trigger_2 = True
  
  s_type_lower = s_type.lower()
  s_target_lower = s_target.lower()
  
  # NEED - fix the invalid response so that it communicates what needs to be changed

  # an if statement that will translate s_target into the correct sorting column based on user input
  while stop_trigger_1 == True:
    if s_target_lower == "math":
      s_target_input = "sat_math_avg_score"
      stop_trigger_1 = False
    elif s_target_lower == "writing":
      s_target_input = "sat_writing_avg_score"
      stop_trigger_1 = False
    elif s_target_lower == "critical reading":
      s_target_input = "sat_critical_reading_avg_score"
      stop_trigger_1 = False
    elif s_target_lower == "overall":
      s_target_input = "overall_average_score"
      stop_trigger_1 = False
    else:
      print "Invalid Option"
      s_target = raw_input("What specific sat score are you looking to rank schools by? (math, writing, critical reading, overall)")
  
  # an if statement that sorts scores high-low or low-high based on user input, also ensures that sort is also run on the right column of scores
  # changed the sort value from "overall_average_score" to the value of the s_target_input variable  
  while stop_trigger_2 == True:
    if s_type_lower == "best":
      sorted_raw_data_no_s = raw_data_no_s.sort_values(s_target_input, ascending=False) 
      print sorted_raw_data_no_s[['school_name', s_target_input]][:int(search_size)]
      stop_trigger_2 = False
      return stop_trigger_2
    elif s_type_lower == "worst":
      sorted_raw_data_no_s = raw_data_no_s.sort_values(s_target_input, ascending=True) 
      print sorted_raw_data_no_s[['school_name', s_target_input]][:int(search_size)]
      stop_trigger_2 == False
      return stop_trigger_2
    else:
      print "Invalid Option"
      s_type = raw_input("Are you looking for the best schools or the worst?")
      
      
search_function(search_type,search_target)
    
    