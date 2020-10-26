import pandas as pd
from verb_conjugations import get_verb_crea_frequency

verb_dfs = []

verb_path = "data/verb_list.txt"
df_path = "data/verb_frequencies.csv"

with open(verb_path, 'r') as src:
    verbs = src.readlines()

for verb in verbs:
    print("Getting", verb.strip())
    df = get_verb_crea_frequency(verb.strip())
    verb_dfs.append(df)

print("Saving data...")
df = pd.concat(verb_dfs)
df.to_csv(df_path, index=False)
print("Done!")


