# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:58:42 2026

@author: Htin Lin Naing
"""

import pandas as pd

fifa_df = pd.read_csv("./Python_project/fifa21 raw data v2.csv")
fifa_df.info()
fifa_df.head()
pd.set_option('display.max_columns', None)
fifa_df.head(1)
pd.set_option('display.max_rows', None)
fifa_df.head(1).T
fifa_df.info()
fifa_df.describe()
# Shows the exact data type and memory footprint of every column
fifa_df.info(memory_usage='deep')



###################################
# Replaces spaces with underscores AND makes everything lowercase
fifa_df.columns = fifa_df.columns.str.replace(' ', '_').str.lower()
fifa_df.rename(columns={'↓ova': 'ova'}, inplace=True)



##################################
# Returns True if all values are different, False if there are duplicates
fifa_df['id'].nunique() == len(fifa_df) # no duplications
fifa_df.isnull().sum()


##################################
fifa_df['nationality'].value_counts()
fifa_df['nationality'] = fifa_df['nationality'].str.strip().astype('category')



########################################
fifa_df['club'].head()
fifa_df['club'].value_counts()
fifa_df['club'] = fifa_df['club'].str.strip().astype('category')



#######################################
fifa_df['contract'].value_counts()

fifa_df['contract_start'] = fifa_df['contract'].astype(str).mask(~fifa_df['contract'].astype(str).str.contains('~')).str.extract(r'(\d{4})')

# 2. End Year: Grabs the LAST 4-digit number found in the string, regardless of format
fifa_df['contract_end'] = fifa_df['contract'].astype(str).str.extract(r'.*(\d{4})')

# 3. Status Column (Handles case-insensitive matches for safety)
status = pd.Series('Contract', index=fifa_df.index)
status = status.mask(fifa_df['contract'].astype(str).str.contains('Loan', case=False), 'On Loan')
status = status.mask(fifa_df['contract'].astype(str).str.strip().str.lower() == 'free', 'Free Agent')

fifa_df['contract_status'] = status.astype('category')

fifa_df = fifa_df.drop(columns=['contract'])




###################################
fifa_df['positions'].value_counts()
fifa_df['positions'] = fifa_df['positions'].str.split(',').explode('positions')
fifa_df['positions'] = fifa_df['positions'].str.strip().astype('category')
fifa_df['positions'].head()

fifa_df['best_position'].value_counts()
fifa_df['best_position'] = fifa_df['best_position'].str.strip().astype('category')
###################################
fifa_df['height'].value_counts()

# 1. Identify which rows are imperial (contain a single quote)
is_imp = fifa_df['height'].str.contains("'", na=False)

# 2. Convert only the imperial rows to centimeters
ft_in = fifa_df.loc[is_imp, 'height'].str.replace('"', '').str.split("'", expand=True).astype(float)
fifa_df.loc[is_imp, 'height'] = (ft_in[0] * 30.48) + (ft_in[1] * 2.54)

# 3. Strip 'cm' from the rest and convert everything to integers
fifa_df['height'] = pd.to_numeric(fifa_df['height'].astype(str).str.replace('cm', '')).round().astype(int)
fifa_df['height'].value_counts()



###############################
fifa_df['weight'].value_counts()
is_lbs = fifa_df['weight'].str.contains("lbs", na=False)

fifa_df.loc[is_lbs, 'weight'] = fifa_df.loc[is_lbs, 'weight'].str.replace('lbs', '').astype(float) * 0.453592

# 3. Strip 'kg' from the metric rows, convert the whole column to numbers, and round it
fifa_df['weight'] = pd.to_numeric(fifa_df['weight'].astype(str).str.replace('kg', '')).round().astype(int)
fifa_df['weight'].value_counts()



###################################
fifa_df.loc[:, 'weight':].head().T
# 1. Convert the column into a proper pandas datetime object
fifa_df['joined'] = pd.to_datetime(fifa_df['joined'])
fifa_df['joined'].info()

fifa_df['loan_date_end'] = pd.to_datetime(fifa_df['loan_date_end'])
fifa_df['loan_date_end'].info()



#################################
fifa_df.loc[:, 'joined':].head().T
fifa_df['value'].value_counts()
fifa_df.rename(columns={'value': 'value_euro'}, inplace=True)
# 1. Clean the text symbols and convert them to numbers
multipliers = fifa_df['value_euro'].str.replace('€', '').str.replace('M', 'e6').str.replace('K', 'e3')

# 2. Convert to numbers (pandas handles scientific e6/e3 text automatically)
fifa_df['value_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['value_euro'].value_counts()



###########################################
fifa_df.loc[:, 'value_euro':].head().T
fifa_df['wage'].value_counts()
fifa_df.rename(columns={'wage': 'wage_euro'}, inplace=True)
# 1. Clean the text symbols and convert them to numbers
multipliers = fifa_df['wage_euro'].str.replace('€', '').str.replace('K', 'e3')

# 2. Convert to numbers (pandas handles scientific e6/e3 text automatically)
fifa_df['wage_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['wage_euro'].value_counts()



#############################################
fifa_df.loc[:, 'wage_euro':].head().T
fifa_df['release_clause'].value_counts()
fifa_df.rename(columns={'release_clause': 'release_clause_euro'}, inplace=True)
# 1. Clean the text symbols and convert them to numbers
multipliers = fifa_df['release_clause_euro'].str.replace('€', '').str.replace('M', 'e6').str.replace('K', 'e3')

# 2. Convert to numbers (pandas handles scientific e6/e3 text automatically)
fifa_df['release_clause_euro'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['release_clause_euro'].value_counts()



############################################# W/F, SM, IR
fifa_df.loc[:, 'release_clause_euro':].head().T
fifa_df.loc[:, 'release_clause_euro':].info()
fifa_df['w/f'] = fifa_df['w/f'].str.replace(r'[^\d]', '', regex=True).astype('category')
fifa_df['sm'] = fifa_df['sm'].str.replace(r'[^\d]', '', regex=True).astype('category')
fifa_df['ir'] = fifa_df['ir'].str.replace(r'[^\d]', '', regex=True).astype('category')
fifa_df.loc[:, 'w/f':].head().T
fifa_df.info()



#################################################
fifa_df['preferred_foot'] = fifa_df['preferred_foot'].astype('category')
fifa_df['a/w'] = fifa_df['a/w'].astype('category')
fifa_df['d/w'] = fifa_df['d/w'].astype('category')



##################################################
fifa_df['hits'].value_counts()
multipliers = fifa_df['hits'].str.replace('K', 'e3')

fifa_df['hits'] = pd.to_numeric(multipliers, errors='coerce').fillna(0).astype(int)
fifa_df['hits'].value_counts()



##################################################
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


fifa_df = fifa_df.astype(data_types)

fifa_df.info(memory_usage='deep')




######################################################################
######################################################################
# Saves the DataFrame as a CSV file without including the index row numbers
fifa_df.to_csv('fifa_cleaned.csv', index=False)

# Saves the DataFrame directly into a standard Excel spreadsheet
fifa_df.to_excel('fifa_cleaned.xlsx', index=False)

# Save your cleaned dataframe along with its metadata
fifa_df.to_pickle("fifa_cleaned.pkl")


import sqlite3

# 1. Temporarily push the DataFrame into a blank in-memory database
with sqlite3.connect(":memory:") as conn:
    fifa_df.to_sql("players", conn, index=False)

    # 2. Automatically dump the entire SQL script directly into a file
    with open("fifa_cleaned.sql", "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in conn.iterdump()) 


