# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:58:42 2026

@author: Htin Lin Naing
"""

import pandas as pd

# Load the FIFA dataset from the CSV file
fifa_df = pd.read_csv("./Python_project/fifa21 raw data v2.csv")

# Display basic info about the dataset - column names, data types, and missing values
fifa_df.info()

# Show the first few rows to get a quick look at the data
fifa_df.head()

# Expand pandas display options to see all columns at once (not truncated)
pd.set_option('display.max_columns', None)
fifa_df.head(1)

# Show all rows when displaying (useful for checking columns vertically)
pd.set_option('display.max_rows', None)

# Transpose the first row to see all columns and their values vertically
fifa_df.head(1).T

# Get detailed info about the dataframe structure
fifa_df.info()

# Display statistical summary of numeric columns
fifa_df.describe()

# Shows the exact data type and memory footprint of every column
fifa_df.info(memory_usage='deep')



###################################
# STEP 1: CLEAN COLUMN NAMES
###################################
# Replaces spaces with underscores AND makes everything lowercase
fifa_df.columns = fifa_df.columns.str.replace(' ', '_').str.lower()

# Fix the special character in one of the column names
fifa_df.rename(columns={'↓ova': 'ova'}, inplace=True)



##################################
# STEP 2: CHECK FOR DUPLICATES AND MISSING VALUES
##################################
# Returns True if all values are different, False if there are duplicates
fifa_df['id'].nunique() == len(fifa_df) # no duplications

# Count how many missing values exist in each column
fifa_df.isnull().sum()


##################################
# STEP 3: CLEAN NATIONALITY COLUMN
##################################
# See which nationalities appear most frequently in the dataset
fifa_df['nationality'].value_counts()

# Remove extra whitespace from country names and convert to category for memory efficiency
fifa_df['nationality'] = fifa_df['nationality'].str.strip().astype('category')



########################################
# STEP 4: CLEAN CLUB COLUMN
########################################
# Check which clubs have the most players
fifa_df['club'].head()
fifa_df['club'].value_counts()

# Clean whitespace and convert to category type to save memory
fifa_df['club'] = fifa_df['club'].str.strip().astype('category')



#######################################
# STEP 5: PARSE CONTRACT INFORMATION
#######################################
# Look at the various contract formats in the data
fifa_df['contract'].value_counts()

# Extract the START year: Grab the first 4-digit number from the contract string
fifa_df['contract_start'] = fifa_df['contract'].astype(str).mask(~fifa_df['contract'].astype(str).str.contains('~')).str.extract(r'(\d{4})')

# Extract the END year: Grab the LAST 4-digit number found in the string, regardless of format
fifa_df['contract_end'] = fifa_df['contract'].astype(str).str.extract(r'.*(\d{4})')

# Create a status column that categorizes the type of contract agreement
# Initialize all values as 'Contract' by default
status = pd.Series('Contract', index=fifa_df.index)

# Update any entries containing 'Loan' to 'On Loan' (case-insensitive)
status = status.mask(fifa_df['contract'].astype(str).str.contains('Loan', case=False), 'On Loan')

# Update any entries that are exactly 'Free' to 'Free Agent'
status = status.mask(fifa_df['contract'].astype(str).str.strip().str.lower() == 'free', 'Free Agent')

# Add the new status column and convert to category to save memory
fifa_df['contract_status'] = status.astype('category')

# Remove the original contract column since we've extracted all useful info from it
fifa_df = fifa_df.drop(columns=['contract'])




###################################
# STEP 6: CLEAN PLAYER POSITIONS
###################################
# Count how many players play each position
fifa_df['positions'].value_counts()

# Some players have multiple positions (e.g., "CB, LB") - split them into separate rows
fifa_df['positions'] = fifa_df['positions'].str.split(',').explode('positions')

# Clean whitespace from position codes and convert to category type
fifa_df['positions'] = fifa_df['positions'].str.strip().astype('category')
fifa_df['positions'].head()

# Check the distribution of best positions
fifa_df['best_position'].value_counts()

# Clean whitespace and convert to category
fifa_df['best_position'] = fifa_df['best_position'].str.strip().astype('category')

###################################
# STEP 7: STANDARDIZE HEIGHT TO CENTIMETERS
###################################
# See what height formats are in the data (imperial vs metric)
fifa_df['height'].value_counts()

# Identify which rows are in imperial format (contain a single quote: 5'10")
is_imp = fifa_df['height'].str.contains("'", na=False)

# For imperial measurements: convert feet and inches to centimeters
# Example: 5'10" becomes (5 * 30.48) + (10 * 2.54) cm
ft_in = fifa_df.loc[is_imp, 'height'].str.replace('"', '').str.split("'", expand=True).astype(float)
fifa_df.loc[is_imp, 'height'] = (ft_in[0] * 30.48) + (ft_in[1] * 2.54)

# For metric measurements: remove 'cm' text and convert to integers
fifa_df['height'] = pd.to_numeric(fifa_df['height'].astype(str).str.replace('cm', '')).round().astype(int)
fifa_df['height'].value_counts()



###############################
# STEP 8: STANDARDIZE WEIGHT TO KILOGRAMS
###############################
# Check the current weight values and formats in the data
fifa_df['weight'].value_counts()

# Identify rows that use pounds (lbs) instead of kilograms (kg)
is_lbs = fifa_df['weight'].str.contains("lbs", na=False)

# Convert pounds to kilograms using the standard conversion factor (1 lbs = 0.453592 kg)
fifa_df.loc[is_lbs, 'weight'] = fifa_df.loc[is_lbs, 'weight'].str.replace('lbs', '').astype(float) * 0.453592

# Remove 'kg' from the metric rows, convert the whole column to numbers, and round it
fifa_df['weight'] = pd.to_numeric(fifa_df['weight'].astype(str).str.replace('kg', '')).round().astype(int)
fifa_df['weight'].value_counts()



###################################
# STEP 9: CONVERT DATE COLUMNS TO DATETIME
###################################
# Display a sample of remaining columns
fifa_df.loc[:, 'weight':].head().T

# Convert the 'joined' column into a proper pandas datetime object for date calculations
fifa_df['joined'] = pd.to_datetime(fifa_df['joined'])
fifa_df['joined'].info()

# Convert the loan end date to datetime format
fifa_df['loan_date_end'] = pd.to_datetime(fifa_df['loan_date_end'])
fifa_df['loan_date_end'].info()



#################################
# STEP 10: CLEAN FINANCIAL COLUMNS (VALUE)
#################################
# Display updated columns
fifa_df.loc[:, 'joined':].head().T

# Check the various value formats (€5M, €500K, etc.)
fifa_df['value'].value_counts()

# Rename the column to be more descriptive
fifa_df.rename(columns={'value': 'value_euro'}, inplace=True)

# Clean the text symbols and convert them to numeric notation:
# Replace € with nothing, M with "e6" (million), K with "e3" (thousand)
multipliers = fifa_df['value_euro'].str.replace('€', '').str.replace('M', 'e6').str.replace('K', 'e3')

# Convert the scientific notation strings to actual numbers, handle any errors
fifa_df['value_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['value_euro'].value_counts()



###########################################
# STEP 11: CLEAN FINANCIAL COLUMNS (WAGE)
###########################################
# Look at what the updated data looks like
fifa_df.loc[:, 'value_euro':].head().T

# Check the wage values and their formats
fifa_df['wage'].value_counts()

# Rename for clarity
fifa_df.rename(columns={'wage': 'wage_euro'}, inplace=True)

# Clean symbols: remove € and convert K (thousands) to scientific notation
multipliers = fifa_df['wage_euro'].str.replace('€', '').str.replace('K', 'e3')

# Convert to numeric values
fifa_df['wage_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['wage_euro'].value_counts()



#############################################
# STEP 12: CLEAN FINANCIAL COLUMNS (RELEASE CLAUSE)
#############################################
# Display the updated financial columns
fifa_df.loc[:, 'wage_euro':].head().T

# Check the release clause values
fifa_df['release_clause'].value_counts()

# Rename for consistency
fifa_df.rename(columns={'release_clause': 'release_clause_euro'}, inplace=True)

# Clean symbols: remove € and convert M and K to scientific notation
multipliers = fifa_df['release_clause_euro'].str.replace('€', '').str.replace('M', 'e6').str.replace('K', 'e3')

# Convert to numeric values
fifa_df['release_clause_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['release_clause_euro'].value_counts()



############################################# 
# STEP 13: CLEAN SKILL RATING COLUMNS (W/F, SM, IR)
#############################################
# Display the last financial column and onwards
fifa_df.loc[:, 'release_clause_euro':].head().T

# Check the data types of the remaining columns
fifa_df.loc[:, 'release_clause_euro':].info()

# Extract only the numeric rating from skill columns (W/F = Weak Foot, SM = Skill Moves, IR = International Reputation)
# Remove all non-digit characters, keeping only the rating number
fifa_df['w/f'] = fifa_df['w/f'].str.replace(r'[^\d]', '', regex=True).astype('category')
fifa_df['sm'] = fifa_df['sm'].str.replace(r'[^\d]', '', regex=True).astype('category')
fifa_df['ir'] = fifa_df['ir'].str.replace(r'[^\d]', '', regex=True).astype('category')

# Display cleaned skill columns
fifa_df.loc[:, 'w/f':].head().T

# Final check on data types after all transformations
fifa_df.info()



#################################################
# STEP 14: CATEGORIZE REMAINING CATEGORICAL COLUMNS
#################################################
# Convert preferred foot to category (Left/Right)
fifa_df['preferred_foot'] = fifa_df['preferred_foot'].astype('category')

# Attacking/Weak foot tendency
fifa_df['a/w'] = fifa_df['a/w'].astype('category')

# Defensive/Weak foot tendency
fifa_df['d/w'] = fifa_df['d/w'].astype('category')



##################################################
# STEP 15: CLEAN THE HITS COLUMN (POPULARITY)
##################################################
# Check the hit counts (popularity metric) - formatted with K for thousands
fifa_df['hits'].value_counts()

# Convert K notation to scientific notation (e3 = thousand)
multipliers = fifa_df['hits'].str.replace('K', 'e3')

# Convert to integers
fifa_df['hits'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['hits'].value_counts()



##################################################
# STEP 16: OPTIMIZE DATA TYPES FOR MEMORY EFFICIENCY
##################################################
# Define the optimal data type for each column to minimize memory usage
# Int8 for small integer ranges (0-127 or -128 to 127), Int16 for medium ranges, Int32 for larger values
data_types = {'age': 'Int8', 'ova': 'Int8', 'pot': 'Int8', 'bov': 'Int8',
              'pac': 'Int8', 'sho': 'Int8', 'pas': 'Int8', 'dri': 'Int8',
              'def': 'Int8', 'phy': 'Int8', 'crossing': 'Int8', 'finishing': 'Int8',
              'heading_accuracy': 'Int8', 'short_passing': 'Int8','volleys': 'Int8',
              'dribbling': 'Int8', 'curve': 'Int8', 'fk_accuracy': 'Int8', 'long_passing': 'Int8',
              'ball_control': 'Int8', 'acceleration': 'Int8', 'sprint_speed': 'Int8', 
              'agility': 'Int8', 'reactions': 'Int8', 'balance': 'Int8', 'shot_power': 'Int8',
              'jumping': 'Int8', 'stamina': 'Int8', 'strength': 'Int8', 'long_shots': 'Int8',
              'aggression': 'Int8', 'interceptions': 'Int8', 'positioning': 'Int8', 'vision': 'Int8',
              'penalties': 'Int8', 'composure': 'Int8', 'marking': 'Int8', 'standing_tackle': 'Int8',
              'sliding_tackle': 'Int8', 'gk_diving': 'Int8', 'gk_handling': 'Int8',
              'gk_kicking': 'Int8', 'gk_positioning': 'Int8', 'gk_reflexes': 'Int8',
                  
              'height': 'Int16', 'weight': 'Int16', 'attacking': 'Int16', 'skill': 'Int16',
              'movement': 'Int16', 'power': 'Int16', 'mentality': 'Int16', 'defending': 'Int16', 
              'goalkeeping': 'Int16', 'base_stats': 'Int16', 'contract_start': 'Int16', 
              'contract_end': 'Int16',
    
              'id': 'Int32', 'total_stats': 'Int32', 'value_euro': 'Int32', 'wage_euro': 'Int32', 
              'release_clause_euro': 'Int32', 'hits': 'Int32'
              }


# Apply the optimized data types to all columns
fifa_df = fifa_df.astype(data_types)

# Display memory usage information after optimization
fifa_df.info(memory_usage='deep')




######################################################################
######################################################################
# STEP 17: EXPORT CLEANED DATA IN MULTIPLE FORMATS
######################################################################

# Saves the DataFrame as a CSV file without including the index row numbers
fifa_df.to_csv('fifa_cleaned.csv', index=False)

# Saves the DataFrame directly into a standard Excel spreadsheet format
fifa_df.to_excel('fifa_cleaned.xlsx', index=False)

# Save the cleaned dataframe as a pickle file (preserves Python data structures)
fifa_df.to_pickle("fifa_cleaned.pkl")


import sqlite3

# Create an SQL database from the cleaned data
# 1. Temporarily push the DataFrame into a blank in-memory database for conversion
with sqlite3.connect(":memory:") as conn:
    fifa_df.to_sql("players", conn, index=False)

    # 2. Automatically dump the entire SQL script directly into a file for backup/sharing
    with open("fifa_cleaned.sql", "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in conn.iterdump()) 

