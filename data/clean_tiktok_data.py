import pandas as pd

def clean_tiktok_data(file):
    with open(file, 'r') as txt:
        lines = txt.readlines()
        
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != 'Follow back' and line != 'Friends'] # remove extra data
    lines = [lines[i] for i in range(len(lines)) if i % 2 != 0] # only keep every other one - keep unique_id, disgard nickname
    lines.reverse() # currently order in stack, reverse to order in a queue
    
    tiktok_usernames = pd.DataFrame({'username': lines})
    
    return tiktok_usernames.to_csv('tiktok_followers.csv', index=False)

clean_tiktok_data("tiktok_followers.txt")