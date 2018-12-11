'''
This will be the basis of each tax database:
TaxYear
STATE
ZIPCODE
agi_stub
NumOfReturns (key: N1)
NumOfSingleReturns (key: MARS1)
NumOfJointReturns (key: MARS2)
NumOfHoHReturns (key: MARS4)
AGI (key: A00100)
NumTaxIncome (key: N04800)
TaxIncomeAmt (key: A04800)
NumAMT (key: N09600)
AMTAmt (key: A09600)
NumWithIncomeTax (key: N06500)
IncomeTaxAmt (key: A06500)
NumTaxLiability (key: N10300)
TaxLiabAmt (key: A10300)
NumTaxDue (key: N11901)
TaxDueAmt (key: A11901)
NumOverpay (key: N11902)
OverpayAmt (key: A11902)


I want to create a second table on just Itemized (Schedule A) data with the following:
STATE
ZIPCODE
agi_stub
NumReturnsWithItem (key: N04470)
TotalItemAmt (key: A04470)
NumWithMedDeductions (key: N17000)
MedDeductionAmt (key: A17000)
NumSLITax (key: N18425)
SLITaxAmt (key: A18425)
NumSalesTax (key: N18450)
SalesTaxAmt (key: A18450)
NumRETax (key: N18500)
RETaxAmt (key: A18500)
NumPropTax (key: N18800)
PropTaxAmt (key: A18800)
NumMortInt (key: N19300)
MortIntAmt (key: N19500)
NumCharitable (key: N19700)
CharitableAmt (key: A19700)
NumLimMiscDed (key: N20800)
LimMiscDedAmt (key: A20800)
NumNonLimMisc (key: N21020)
NonLimMiscAmt (key: A21020)


Lastly, a (selected) credit table:
STATE
ZIP
agi_stub
NumEIC (key: N59660)
EICAmt (key: A59660)
NumEdCred (key: N10960)
EdCredAmt (key: A10960)

'''

fileList = ['Individual Tax Stats by Zip 2016.csv','Individual Tax Stats by Zip 2015.csv','Individual Tax Stats by Zip 2014.csv','Individual Tax Stats by Zip 2013.csv']
SchAList = ['STATE','ZIPCODE','AGI_STUB','N04470','A04470','N18425','A18425','N18450','A18450','N18500','A18500','N19300','A19300','N19700','A19700']
TaxList = ['STATE', 'ZIPCODE', 'agi_stub', 'N1', 'MARS1', 'MARS2', 'MARS4', 'A00100', 'N04800', 'A04800', 'N09600',
               'A09600', 'N06500', 'A06500', 'N10300', 'A10300', 'N11901', 'A11901', 'N11902', 'A11902']
CredList = ['STATE','zipcode','AGI_STUB','N59660','A59660','N10960','A10960']
import csv
import pandas as pd
from sqlalchemy import create_engine
import pyodbc

for fileName in fileList:
    
    
    with open(fileName, 'r+', encoding='utf8') as file:
        data = pd.read_csv(file)
        
        #First, the general Tax Year Table
        TaxYrTable = pd.DataFrame()
        
        for item in TaxList:
            try:
                TaxYrTable.insert(loc=len(TaxYrTable.columns), column=item, value=data[item])
            except:
                TaxYrTable.insert(loc=len(TaxYrTable.columns), column=item.lower(),value=data[item.lower()])
            
        #Now the Sch A Table
        SchATable = pd.DataFrame()
        
        for item in SchAList:
            try:
                SchATable.insert(loc=len(SchATable.columns),column=item,value=data[item])
            except:
                SchATable.insert(loc=len(SchATable.columns),column=item.lower(),value=data[item.lower()])
        #Last, the Credits Table
        CreditTable = pd.DataFrame()
           
        for item in CredList:
            try:
                CreditTable.insert(loc=len(CreditTable.columns),column=item,value=data[item])
            except:
                CreditTable.insert(loc=len(CreditTable.columns),column=item.lower(),value=data[item.lower()])
                
    #Now we are renaming the columns to more logical names that can be more easily queried        
    TaxYrTable.rename(
        columns={'STATE': 'STATE', 'zipcode': 'ZIPCODE', 'N1': 'NumOfReturns', 'mars1': 'NumOfSingleReturns',
                 'MARS2': 'NumOfJointReturns', 'MARS4': 'NumHOHReturns', 'A00100': 'AGI', 'N04800': 'NumTaxIncome',
                 'A04800': 'TaxIncomeAmt', 'N09600': 'NumAMT', 'A09600': 'AMTAmt', 'N06500': 'NumWithIncomeTax',
                 'A06500': 'IncomeTaxAmt', 'N10300': 'NumTaxLiab', 'A10300': 'TaxLiabAmt', 'N11901': 'NumTaxDue',
                 'A11901': 'TaxDueAmt', 'N11902': 'NumOverpay', 'A11902': 'OverpayAmt'}, inplace=True)
    yr = fileName[-8:-4]
    TaxYrTable.insert(column='TaxYear',value=str(yr),allow_duplicates=True,loc=0)
    xlFileName = 'Tax_Data_' + str(yr) + '.xlsx'
    TaxYrTable.to_excel(xlFileName)
    
    SchATable.rename(columns ={'STATE':'STATE','zipcode':'ZIPCODE','agi_stub':'agi_stub',
                               'N04470':'NumReturnsWithItem','A04470':'TotalItemAmt','N18425':'NumSLITax',
                               'A18425':'SLITaxAmt','N18450':'NumSalesTax','A18450':'SalesTaxAmt',
                               'N18500':'NumRETax','A18500':'RETaxAmt','N19300':'NumMortInt',
                               'A19300':'MortIntAmt','N19700':'NumCharitable',
                               'A19700':'CharitableAmt'},inplace=True)

    SchATable.insert(column='TaxYear',value=yr,allow_duplicates=True,loc=0)


    
    AFileName = 'Sch_A_Data_' + str(yr) + '.xlsx'
    SchATable.to_excel(AFileName)
    
    
    CreditTable.rename(columns ={'STATE':'STATE','zipcode':'ZIPCODE','agi_stubs':'agi_stubs','N59660':'NumEIC',
                              'A59660':'EICAmt','N10960':'NumEdCred','A10960':'EdCredAmt'},inplace=True)

    CreditTable.insert(column='TaxYear',value=yr,allow_duplicates=True,loc=0)
    CredFileName = 'Credit_Data_' + str(yr) + '.xlsx'
    CreditTable.to_excel(CredFileName)
    
    '''Originally I used this code to persist my data to a SQL server hosted on Azure. This became way too
    difficult to keep doing because each time I tried to publish a table to my server, it took 3-4 hours
    to finish running. I did the first table that way, but I was not about to do that for 3 tables for
    each of 4 tax years. Instead, I persisted my data to excel and then imported it directly through
    SQL Server Management Studio. The code to persist my data was pretty short, here it is:'''
    #engine = create_engine('mssql+pyodbc://ButtrmlkPncakes@cody-practice.database.windows.net:Avalon09!@cody-practice.database.windows.net/Cody-IRS-Data?driver=SQL+Server+Native+Client+11.0',echo=True,connect_args={'interactive_timeout':30000,'wait_timeout':30000})
    #con = engine.connect()
    #TaxYrTable.to_sql(xlFileName,con=con,if_exists='replace',chunksize=1000)
    #SchATable.to_sql(AFileName,con=con,if_exists='replace',chunksize=1000)
    #CreditTable.to_sql(CredFileName,con=con,if_exists='replace',chunksize=1000)
    '''Simple as that! simply make your connection string, then use Pandas' to_sql function instead of
    the to_excel function. I used a chunksize of 1000 because the connection would time out otherwise.
    As an aside, I also went into SQL server and changed the data types to smaller types because otherwise
    it turned into the largest data type possible.'''
