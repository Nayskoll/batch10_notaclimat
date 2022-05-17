import pandas as pd
import base64

# functions

def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 

# Generating company_id variable

import base64
def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 

cols_for_calculation = [
    'company_name',
    'C1 direct score',
    'C1 initial value',
    'C1 final value', 
    'C1 unit', 
    'C1 initial date',
    'C1 final date', 
    'C1 2deg final', 
    'C1 1,8deg final',
    'C1 1,5deg final',
    'C2 complete score', 
    'C2 complete level',
    'C2 reduction',
    'C2 initial value', 
    'C2 final value',
    'C2 unit',
    'C2 initial date',
    'C2 final date', 
    'C2 2deg final',
    'C2 1,8deg final',
    'C2 1,5deg final'
]


# variables
# For global score references
list_reference = ['Unrevealed', 'TotallyInsufficient', 'Insufficient', 'Partial', 'Strong', 'VeryStrong']

# For C1 and C2 direct scores references
list_reference2 = ['Non publiée', 'Vers + 4°C', 'Entre +2°C et +3°C', '2°C', 'Bien moins de 2°C', '1,5°C', 'n.a. (trop récente)']
list_hexcolors_direct = ['#820000', '#C00000', '#FF8939', '#FEC800', '#8CDF41', '#0DB800', '#C00000']
list_scores = ['1','2','3','4','5','6','99']


# Extract origin table

df = pd.read_excel("../data/BDD Surcouche pour dataviz_v03.xlsx")
df = df.drop([0])

# Pre-treatment

t1b2_data = df.rename(columns={'Group':'company_name'})
t1b2_data['company_id'] = [encode(x) for x in t1b2_data['company_name']]


# Calculating score performance to choose color
direct_score_reference_table = pd.DataFrame(
  data={
    'direct_score': list_scores, 
    'direct_score_label': list_reference2, 
    'hexcolor':list_hexcolors_direct
    }
  )

   
# Filtering data & adding reference columns

df_filtered = t1b2_data[cols_for_calculation].copy()

df_filtered= df_filtered.astype(
  {'C1 direct score': int, 
   'C2 complete score': int
  }
).astype(
  {'C1 direct score': str, 
   'C2 complete score': str
  }
)    


# C1 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='C1 direct score', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'c1_label', 'hexcolor': 'c1_color'}
).drop(
  columns=['direct_score']
)
  
  
# C2 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='C2 complete score', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'c2_label', 'hexcolor': 'c2_color'}
).drop(
  columns=['direct_score']
)


# Adding the global score image
# TODO
# df_filtered['global_score_pic'] = 'assets/frames/climate_score/Frame_'+ df_filtered['global_score_label']+'.png' 


# Updating column names to match variables list
# TODO
df_filtered = df_filtered.rename(
  columns={
    'C1 direct score': 'direct_score',
    'c1_label': 'direct_score_short_label',
    'c1_color': 'direct_score_hexa_color_code',
    'C2 complete score': 'complete_score',
    'c2_label': 'complete_score_short_label',
    'c2_color': 'complete_score_hexa_color_code'
  })

# Exporting
df_filtered.to_csv(
  path_or_buf='t1b2.csv',
  sep=',', 
  header=True, 
  index=False
)