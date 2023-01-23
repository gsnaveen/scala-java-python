
# coding: utf-8

# In[76]:


import pandas as pd
import dateutil.parser
import re

import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go
import numpy as np
import cufflinks as cf
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)
cf.go_offline()
get_ipython().magic('matplotlib inline')
from ipywidgets import *
from IPython.display import display
#from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

#DFAgentMap['END_DATE'] = DFAgentMap.END_DATE.apply(lambda x: x if not pd.isnull(x) else '1/1/2000')
DFloans = pd.read_csv('Loan Data.csv')
DFAgentLoans = pd.read_csv('Agent Loans.csv')
DFAgentMap = pd.read_csv('Agent Map.csv')
#Joining loan and agent
df = DFloans.merge(DFAgentLoans,how='inner',left_on='id',right_on='ID')
#converting date fields as date datatypes
df['decision_d'] = df['decision_d'].apply(lambda x: dateutil.parser.parse(x))
df['last_pymnt_d'] = df.last_pymnt_d.apply(lambda x: '12/12/2100' if pd.isnull(x) else x)
df['last_pymnt_d'] = df['last_pymnt_d'].apply(lambda x: dateutil.parser.parse(x))
df['next_pymnt_d'] = df.next_pymnt_d.apply(lambda x: '12/12/2100' if pd.isnull(x) else x)
df['next_pymnt_d'] = df['next_pymnt_d'].apply(lambda x: dateutil.parser.parse(x))
DFAgentMap['START_DATE'] = DFAgentMap['START_DATE'].apply(lambda x: dateutil.parser.parse(x))
DFAgentMap['END_DATE'] = DFAgentMap.END_DATE.apply(lambda x: '12/12/2100' if x == '12/12/2999' else x)
DFAgentMap['END_DATE'] = DFAgentMap['END_DATE'].apply(lambda x: dateutil.parser.parse(x))
#joining Agent details 
df = df.merge(DFAgentMap,how='inner',left_on='AGENT_NUMBER',right_on='AGENT_ID')

def setFlag(row):
    return 'Yes' if row['decision_d'] >= row['START_DATE'] and row['decision_d'] <= row['END_DATE'] else 'No'

#setting up the flag for the SKILL_LEVEL 	TEAM 	START_DATE 	END_DATE
df['flag'] = df.apply(setFlag, axis=1)
df = df[df.flag == 'Yes'].reset_index() # filtering only the valid records

#compute > 60 days in role
df['ddays'] = (df['decision_d'] - df['START_DATE']).dt.days
df['flag60'] = df.ddays.apply(lambda x : 'Yes' if x > 60 else 'No' )
df['termnum'] = df.term.apply(lambda x : int(x.strip().split(' ')[0]))
df['int_ratenum'] = df.int_rate.apply(lambda x : float(re.sub('%','',x.strip())))
df.drop('AGENT_NUMBER', axis=1, inplace=True)
df['counter'] = 1


# In[77]:


df.dtypes


# In[78]:


df.to_csv('mydata.tsv',sep='\t',index=False)


# In[79]:


#Current skills of teams
DFAgentMap[DFAgentMap.END_DATE == '2100-12-12'].groupby(['TEAM','SKILL_LEVEL'])['END_DATE'].count().reset_index().pivot_table(index='SKILL_LEVEL',columns='TEAM',values='END_DATE').reset_index().fillna(0)


# In[80]:


dfplot = df.groupby(['decision_d'])['counter'].count().reset_index().set_index('decision_d').rename(columns={'counter':'#OfLoans'})
fig1 = dfplot.iplot(columns=['#OfLoans'],kind='line', asFigure=True,title='Monthly Loan Trend',colors='green', yTitle='#OfLoan')

dfplot = df.groupby(['decision_d'])['loan_amnt'].sum().reset_index().set_index('decision_d')
fig2 = dfplot.iplot(columns=['loan_amnt'], kind='line', secondary_y=['loan_amnt'] , width = 2,asFigure=True,title='Monthly Loan Trend',colors='blue',xTitle='Month/Year', secondary_y_title='AmountOfLoan' )

fig2['data'].extend(fig1['data'])
iplot(fig2)


# In[81]:


#With Secondary Axis
dfplot = df.groupby(['purpose','loan_status'])['counter'].count().reset_index().pivot_table(index=['purpose'],columns='loan_status', values='counter').reset_index().fillna(0).set_index('purpose')
fig1 = dfplot.iplot(columns=['In Grace Period','Late (16-30 days)','Late (31-120 days)'],kind='bar', asFigure=True)
fig2 = dfplot.iplot(columns=['Current'], kind='area', secondary_y=['Current'] , width = 2,asFigure=True,title='Monthly Loan Trend')
# 'Fully Paid','Charged Off'
fig2['data'].extend(fig1['data'])
iplot(fig2)


# In[82]:


#With Secondary Axis
dfplot = df.groupby(['purpose','loan_status'])['counter'].count().reset_index().pivot_table(index=['purpose'],columns='loan_status', values='counter').reset_index().fillna(0).set_index('purpose')
keys = list(dfplot.index)
values = list(dfplot['Current'])
inGrace = list(dfplot['In Grace Period'])
late16 = list(dfplot['Late (16-30 days)'])
late31 = list(dfplot['Late (31-120 days)'])

inGrace = go.Scatter(
    x=keys,
    y=values,
    mode='markers',
    marker=dict(
        size=inGrace,
    )
)

late16 = go.Scatter(
    x=keys,
    y=values,
    mode='markers',
    marker=dict(
        size=late16,
    )
)

late31 = go.Scatter(
    x=keys,
    y=values,
    mode='markers',
    marker=dict(
        size=late31,
    )
)
layout = go.Layout(
    title='Bubbles'
)
data = [inGrace,late16,late31]

iplot(data,filename='bubblechart-size')


# In[83]:


#decision count after 60 days in the role
decisioncount = df[(df.flag60 == 'Yes') ].groupby(['AGENT','flag60'])['counter'].count().reset_index().set_index('AGENT')
dfplot = decisioncount
keys = list(dfplot.index)
values = list(dfplot['counter'])

trace1 = go.Bar(
    x=keys,
    y=values,
    name='Yes'
)

decisioncount = df[(df.flag60 == 'No') ].groupby(['AGENT','flag60'])['counter'].count().reset_index().set_index('AGENT')
dfplot = decisioncount
keys = list(dfplot.index)
values = list(dfplot['counter'])


trace2 = go.Bar(
    x=keys,
    y=values,
    name='No'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='group'
    ,title='Loan Before & After 60 days '
)

fig = go.Figure(data=data, layout=layout)
iplot(fig, filename='grouped-bar')


# In[84]:


#Charged off loans 
chargedOffLoans = df[df.loan_status == 'Charged Off'].groupby(['TEAM','grade'])['counter'].count().reset_index().rename(columns={'counter':'chargedoff'})
totalLoans = df.groupby(['TEAM','grade'])['counter'].count().reset_index().rename(columns= {'counter':'Loans'})
chargedOffLoansPercent = totalLoans.merge(chargedOffLoans,how='left',on=['TEAM','grade'] )
chargedOffLoansPercent['ChargeOffPercent'] = chargedOffLoansPercent['chargedoff'] / chargedOffLoansPercent['Loans']
chargedOffLoansPercent

chargedOffLoans = df[df.loan_status == 'Charged Off'].groupby(['TEAM'])['counter'].count().reset_index().rename(columns={'counter':'chargedoff'})
totalLoans = df.groupby(['TEAM'])['counter'].count().reset_index().rename(columns= {'counter':'Loans'})
chargedOffLoansPercent = totalLoans.merge(chargedOffLoans,how='left',on=['TEAM'] )
chargedOffLoansPercent = chargedOffLoansPercent.set_index('TEAM')
chargedOffLoansPercent['ChargeOffPercent'] = chargedOffLoansPercent['chargedoff'] / chargedOffLoansPercent['Loans']
dfplot = chargedOffLoansPercent
fig1 = dfplot.iplot(columns=['Loans','chargedoff'],kind='bar', asFigure=True)
fig2 = dfplot.iplot(columns=['ChargeOffPercent'], kind='lines', secondary_y=['ChargeOffPercent'], width = 2 ,asFigure=True)
# 'Fully Paid','Charged Off'
fig2['data'].extend(fig1['data'])
iplot(fig2)


# In[85]:


#loan term per agent
avgLoanTermPerAgent = df[(df.flag60 == 'Yes') ].groupby(['AGENT'])['termnum'].mean().reset_index().set_index('AGENT')
dfplot = avgLoanTermPerAgent
fig1 = dfplot.iplot(columns=['termnum'],kind='line', asFigure=True)
iplot(fig1)


# In[86]:


avgLoanTermPerAgent = df[(df.flag60 == 'No') ].groupby(['AGENT'])['termnum'].mean().reset_index().set_index('AGENT')
dfplot = avgLoanTermPerAgent
fig1 = dfplot.iplot(columns=['termnum'],kind='line', asFigure=True)
iplot(fig1)


# In[87]:


dfplot = avgLoanTermPerAgent = df.groupby(['decision_d','grade'])['counter'].sum().reset_index().set_index('decision_d')
dfplot.iplot(kind='heatmap',y='grade',z='counter',colorscale='rdylbu')


# In[88]:


dfplot = df.groupby(['purpose','grade'])['loan_amnt'].sum().reset_index()#.set_index('decision_d') #.reset_index()
dfplot.iplot(kind='bubble',x='purpose',y='grade',size='loan_amnt') #,x='decision_d'


# In[89]:


df.groupby(['decision_d','purpose'])['loan_amnt'].sum().reset_index().pivot_table(index='decision_d',columns='purpose',values='loan_amnt').reset_index().fillna(0).set_index('decision_d').iplot(kind='box')


# In[90]:


df[df.decision_d == '2011-01-01'][['loan_amnt','revol_bal']].reset_index().iplot(kind='spread')


# In[91]:


mydf = df[df.decision_d == '2011-01-01'][['purpose','loan_amnt','revol_bal']].reset_index().drop('index', axis=1).scatter_matrix()
#mydf.drop('index', axis=1, inplace=True)
# mydf.scatter_matrix()


# In[103]:


import ipywidgets as wg
from IPython.display import display
from IPython.display import clear_output

radio = wg.RadioButtons(options=df['purpose'].drop_duplicates().tolist(),description='radioButt')
display(radio)

def on_change(change):
    #clear_output()
    dfplot = df[df.purpose == change['new']].groupby(['decision_d','grade'])['counter'].sum().reset_index().set_index('decision_d')
    dfplot.iplot(kind='heatmap',y='grade',z='counter',colorscale='rdylbu')
    #print()
    
radio.observe(on_change,names='value')


