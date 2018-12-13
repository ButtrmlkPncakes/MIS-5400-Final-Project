# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 17:07:43 2018

@author: Test1
"""

import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import GetCredentials

User,Pass = GetCredentials.GetCreds('its me, dummy','let me in')

#%matplotlib inline

graphList = ['OverpayAmt','TaxDueAmt']

def GetData():
    engine = create_engine(
        'mssql+pyodbc://' + User + '@cody-practice.database.windows.net:' + Pass + '@cody-practice.database.windows.net/Cody-IRS-Data?driver=SQL+Server+Native+Client+11.0',
        echo=True, connect_args={'interactive_timeout': 30000, 'wait_timeout': 30000})
    con = engine.connect()

    df2016 = pd.read_sql('Tax_Data_2016',con=con)
    df2015 = pd.read_sql('Tax_Data_2015',con=con)
    df2014 = pd.read_sql('Tax_Data_2014',con=con)
    df2013 = pd.read_sql('Tax_Data_2013',con=con)
    
    #df2016 = pd.read_excel('Tax_Data_2016.xlsx')
    #df2015 = pd.read_excel('Tax_Data_2015.xlsx')
    #df2014 = pd.read_excel('Tax_Data_2014.xlsx')
    #df2013 = pd.read_excel('Tax_Data_2013.xlsx')
    
    AllYears = [df2016,df2015,df2014,df2013]
    
    dfAll = pd.DataFrame(df2016)
    print(dfAll.columns)
    dfAll = dfAll.append([df2015,df2014,df2013])
    try:
        dfAll = dfAll[dfAll.ZIPCODE != 0]
    except:
        dfAll = dfAll[dfAll.zipcode != 0]
    labels = ['$1\nto\n$25,000','$25,000\nto\n$50,000','$50,000\nto\n$75,000','$75,000\nto\n$100,000','$100,000\nto\n$200,000','$200,000\nor more']
    return dfAll, AllYears,labels

def BarCharts():
#    df = dfAll
    df, AllYears,labels = GetData()
    for cat in graphList:
        
        dataOne = sum(df[df.agi_stub == 1][cat])
        dataTwo = sum(df[df.agi_stub == 2][cat])
        dataThree = sum(df[df.agi_stub == 3][cat])
        dataFour = sum(df[df.agi_stub == 4][cat])
        dataFive = sum(df[df.agi_stub == 5][cat])
        dataSix = sum(df[df.agi_stub == 6][cat])
        YearsDict = {}
        x = 2013
        for item in AllYears:
            data1 = sum(item[item.agi_stub == 1][cat])
            data2 = sum(item[item.agi_stub == 2][cat])
            data3 = sum(item[item.agi_stub == 3][cat])
            data4 = sum(item[item.agi_stub == 4][cat])
            data5 = sum(item[item.agi_stub == 5][cat])
            data6 = sum(item[item.agi_stub == 6][cat])
            newList = [data1,data2,data3,data4,data5,data6]
            YearsDict['df'+ str(x)] = newList
            x += 1
        newestest = [sum(dfAll[dfAll.agi_stub == x]['NumTaxDue']) for x in range(1,7)]
        leny = np.arange(len(labels))
        plt.ticklabel_format(style='plain',axis='y',useOffset=False)
        data = [dataOne,dataTwo,dataThree,dataFour,dataFive,dataSix]
        barlabes = []
        height = max(data)
        plt.bar(leny, data, align='center',width=.5)
        plt.xticks(leny,labels)
        plt.xlabel('AGI Range')
        if cat == 'OverpayAmt':
            plt.title('Tax Overpayment Amounts 2013-2017')
            plt.ylabel('Amount of Overpayment')
        elif cat =='TaxDueAmt':
            plt.title('Tax Due Amounts 2013-2017')
            plt.ylabel('Amount of Tax Due')
        
        fig2,ax2 = plt.subplots()
        
        plt.ticklabel_format(style='plain',axis='y',useOffset=False)
        index = np.arange(6)
        bar_width = .15
        rects1 = plt.bar(leny-bar_width,YearsDict['df2013'],bar_width,label='Tax Year 2013',align='center')
        rects2 = plt.bar(leny,YearsDict['df2014'],bar_width, label='Tax Year 2014',align='center')
        rects3 = plt.bar(leny+bar_width,YearsDict['df2015'],bar_width, label='Tax Year 2015',align='center')
        rects4 = plt.bar(leny+(bar_width*2),YearsDict['df2016'],bar_width, label='Tax Year 2016',align='center')
        plt.xticks(leny,labels)
        plt.xlabel('AGI Range')
        if cat == 'OverpayAmt':
            plt.title('Tax Overpayment Amounts 2013-2017 by Year')
            plt.ylabel('Amount of Overpayment')
        elif cat =='TaxDueAmt':
            plt.title('Tax Due Amounts 2013-2017 by Year')
            plt.ylabel('Amount of Tax Due')
        plt.legend()
        plt.show()
    
    
def HeatMap():
    df, AllYears,labels = GetData()
    StateData = [df['AGI']]
    leny = np.arange(len(labels))
    newFrame = pd.DataFrame(df.STATE)
    TempFrame = pd.DataFrame(df.TaxDueAmt)
    #TempFrame2 = pd.DataFrame(dfAll.TaxYear)
    newerFrame = pd.concat([newFrame,TempFrame],axis=1)
    newestFrame = newerFrame.groupby(['STATE']).sum()
    
    
    import matplotlib.ticker as ticker
    
    sns.set()
    newestFrame = newestFrame.sort_values(['TaxDueAmt'],ascending=False)
    newestFrame = newestFrame.head(10)
    f,ax = plt.subplots(figsize=(10,10))
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    
    sns.heatmap(newestFrame,annot=True)
    plt.xlabel('AGI Range')
    plt.ylabel('Zip Codes with Most Tax Due - ' + str(state))
    plt.xticks(leny,labels)
    #plt.ticklabel_format(style='plain',axis='y')
    
    plt.show()

def HeatMap2(state):
    state = state.upper()
    df, AllYears,labels = GetData()
    leny = np.arange(len(labels))
    StateFrame = df[df.STATE == state]
    StateFrame = StateFrame.loc[:,['ZIPCODE','agi_stub','TaxDueAmt']]
    StateFrame = StateFrame.sort_values(['TaxDueAmt'],ascending=False)
    ZipGroups = StateFrame.groupby(['ZIPCODE'],as_index=False).sum()
    TopZips = ZipGroups.nlargest(10,columns='TaxDueAmt')
    StateFrame = StateFrame[StateFrame.ZIPCODE.isin(TopZips.ZIPCODE)]
    StateFrame.ZIPCODE = pd.to_numeric(StateFrame.ZIPCODE)
    StateFrame.agi_stub = pd.to_numeric(StateFrame.agi_stub)
    StateTable = StateFrame.pivot_table(index='ZIPCODE',columns='agi_stub',values='TaxDueAmt',aggfunc='sum')
    f, ax = plt.subplots(figsize = (9,12))
    sns.heatmap(StateTable,annot=True,ax=ax,linewidths=.5,fmt='d')
    plt.xlabel('AGI Range')
    plt.ylabel('Zip Codes with Most Tax Due - ' + str(state))
    plt.xticks(leny,labels)
    plt.savefig('C:/Users/mes12/Desktop/Fall 2018 - USU/MIS 5400/Final Project/static/HeatMap.jpg')# + str(state) + '.jpg')
    return 'Heat Map successfully created.'

#BarCharts(dfAll)
#HeatMap(dfAll)
#HeatMap2(dfAll)
