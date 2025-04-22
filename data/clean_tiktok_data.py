import pandas as pd

def clean_tiktok_data(file):
    with open(file, 'r') as txt:
        lines = txt.readlines()
        
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != 'Follow back' and line != 'Friends']
    lines = [lines[i] for i in range(len(lines)) if i % 2 != 0]
    
    tiktok_usernames = pd.DataFrame({'Username': lines})
    
    return tiktok_usernames.to_csv('tiktok_followers.csv')

clean_tiktok_data("tiktok_followers.txt")