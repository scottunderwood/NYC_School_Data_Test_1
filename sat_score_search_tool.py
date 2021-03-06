import numpy as np
import pandas as pd
import datetime
import urllib


# source data: https://data.cityofnewyork.us/Education/SAT-Results/f9bf-2cp4
# query removes all of the rows where a school did not report scores, enables later code to change score column datatypes from str to int
query_1 = ("https://data.cityofnewyork.us/resource/734v-jeq5.json?"
         "$where=num_of_sat_test_takers!='s'")
raw_score_data_no_s = pd.read_json(query_1)

# NEED - pull in second directory datafile https://data.cityofnewyork.us/Education/DOE-High-School-Directory-2014-2015/n3p6-zve2
# NEED - find a way to improve the response time on this second pull by filtering out the irrelivant data
# This now is attempt to pull in second directory dataset
query_2 = ("https://data.cityofnewyork.us/resource/2u2u-zka4.json?")
raw_directory_data = pd.read_json(query_2)

# NEED - want to change the column headers to something more readable


# these change the datatype in all of the score columns to int so that I can run calculations off of them  
raw_score_data_no_s['sat_math_avg_score'] = raw_score_data_no_s['sat_math_avg_score'].astype(int)
raw_score_data_no_s['sat_critical_reading_avg_score'] = raw_score_data_no_s['sat_critical_reading_avg_score'].astype(int)
raw_score_data_no_s['sat_writing_avg_score'] = raw_score_data_no_s['sat_writing_avg_score'].astype(int)

# creates a new column in the dataframe and then populate it with the average of the three sat scores
raw_score_data_no_s['overall_average_score'] = (raw_score_data_no_s.sat_writing_avg_score + raw_score_data_no_s.sat_critical_reading_avg_score + raw_score_data_no_s.sat_math_avg_score) / 3


# normalizes the values in the school_name column of both dataframes so that they are uniformly lowercase 
raw_score_data_no_s['school_name'] = map(lambda x: x.lower(), raw_score_data_no_s['school_name'])
raw_directory_data['school_name'] = map(lambda x: x.lower(), raw_directory_data['school_name'])


# merges the raw score data with the raw directory data on the school_name column to produce a single new dataframe
combined_data = pd.merge(raw_directory_data, raw_score_data_no_s, on='school_name', how='inner')


# a title for the tool to appear before the user prompts
print ""
print ""
print "New York City Schools Sorted by Average SAT Scores"
print ""


# user input prompted to indicate which score they want to sort by, if they want highest or lowest scoring schools, and how many to show
# breaking out lines printed in the console further so that they are easier to interact with
print ""
print "What specific sat score are you looking to rank schools by? (math, writing, critical reading, overall)"
search_target = raw_input("Response: ")
print ""
print "Are you looking for the best schools or the worst schools?"
search_type = raw_input("Response: ")
print ""
print "How long a list do you need? "
search_size = raw_input("Response: ")


# NEED - create a function that tests search_size input to make sure its just a number

# NEED - want to add another prompt that gives you a menu of additonal datapoints to include in the printout
# NEED - will require printing a menu of options, validation, and then input into the print function


# a function that prints list of schools based on user input search parameters
def search_function(s_type, s_target):
  
  stop_trigger_1 = True
  stop_trigger_2 = True
  
  s_type_lower = s_type.lower()
  s_target_lower = s_target.lower()
  
  # an if statement that will translate s_target into the correct sorting column based on user input
  # NEED - break search target validation out into its own function, move to immediately after the first prompt
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
      print ""
      print "Invalid selection, please select a test score to rank schools by from the following options (math, writing, critical reading, overall)"
      s_target_lower = raw_input("Response: ")
  
  # an if statement that sorts scores high-low or low-high based on user input, also ensures that sort is also run on the right column of scores
  # changed the sort value from "overall_average_score" to the value of the s_target_input variable 
  # NEED - break search target validation out into its own function, move to immediately after the first prompt
  while stop_trigger_2 == True:
    if s_type_lower == "best":
      # changing all subsequent dataframe names to reflect the new merged dataframe
      sorted_combined_data = combined_data.sort_values(s_target_input, ascending=False) 
      # adding in third output column 'boro' to test the merge
      print sorted_combined_data[['school_name','boro', s_target_input]][:int(search_size)]
      stop_trigger_2 = False
      return stop_trigger_2
    elif s_type_lower == "worst":
      sorted_combined_data = combined_data.sort_values(s_target_input, ascending=True) 
      # adding in third output column 'boro' to test the merge
      print sorted_combined_data[['school_name', 'boro', s_target_input]][:int(search_size)]
      stop_trigger_2 == False
      return stop_trigger_2
    else:
      print ""
      print "Invalid selection, please indicate your desired search type as either 'best' or 'worst'"
      s_type_lower = raw_input("Response: ")
      
      
search_function(search_type,search_target)
    
    