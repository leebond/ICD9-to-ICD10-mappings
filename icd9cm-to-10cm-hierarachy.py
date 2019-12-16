# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:27:49 2019

@author: leebond

This piece of work uses the General Equivalence Mappings file by cms.gov
to convert ICD 9-CM codes to ICD 10-CM codes.

It also stitches the ICD 10-CM codes with the ICD 10-CM descriptions using another 
mapping file provided by cms.gov

Additional
There is also an option to stitch ICD 10-CM hierarchy codes to the ICD 10-CM codes.
The hierarchy data are derived separately by another respository where they had been webscraped from
icd10data.com

There is also an option to stitch ICD 10-CM CCSR categories with the ICD 10-CM codes.
The CCSR mappings are borrowed from hcup-as.ahrq.gov

"""
import re
import pandas as pd
from zipfile import ZipFile

def unzipFile(zip_file, content):
    with ZipFile(zip_file, 'r') as f_zip:
        f_zip.extract(content)
        
def readICD10GEMS(gemfile):
    icd_map = []
    with open(gemfile,'r') as f:
        for line in f:
            icd_map += [line.split()]
    icd10_gems = pd.DataFrame(icd_map).rename(columns={0:'icd9',1:'icd10',2:'flag'})
    return icd10_gems

def readICD10Desc(descfile):
    icd10_desc_list = []
    with open(descfile,'r') as f:
        for line in f:
            line_split = [line.split()[0]] + [' '.join(line.split()[1:])]
            icd10_desc_list += [line_split]
    icd10_desc = pd.DataFrame(icd10_desc_list).rename(columns={0:'icd10',1:'Description'})
    return icd10_desc

def readICD10Hierarchy(file):
    icd10_hier = pd.read_csv(file)
    return icd10_hier

def removeSingleQuotes(row):
    return re.sub("'", "", row)

def readICD10CCSR(file):
    icd10_ccsr = pd.read_csv(file)
    icd10_ccsr["'ICD-10-CM CODE'"] = icd10_ccsr["'ICD-10-CM CODE'"].apply(removeSingleQuotes)
    return icd10_ccsr

def processICD10Code(code):
    icd10list = icd10_desc['icd10'].tolist()
    exist = False
    while exist != True:
        for i in range(10):
            newcode = str(code) + str(i)
            if newcode in icd10list:
                exist = True
                return newcode
            else:
                exist = False
        return None

def processicd10desc(row):
    if row['icd10'] == 'NoDx':
        return 'Conversion Not Available'
    elif row['Description'] == None:
        return 'Missing Description'
    else:
        return row['Description']

def fillNAICD10Desc(icd10_mst):
    icd10_na = icd10_mst[(icd10_mst['Description'].isna())&(icd10_mst['icd10']!='NoDx')]
    icd10_nona = icd10_mst[~((icd10_mst['Description'].isna())&(icd10_mst['icd10']!='NoDx'))]
    
    icd10_na['icd10_pro'] = icd10_na['icd10'].apply(processICD10Code)
    icd10_na_new = pd.merge(icd10_na, icd10_desc, left_on='icd10_pro', right_on='icd10', how='left')
    icd10_na_final = icd10_na_new[['icd9', 'icd10_x', 'flag', 'Description_y']]
    icd10_na_final.columns = ['icd9', 'icd10', 'flag', 'Description']
    icd10_map = icd10_nona.append([icd10_na_final])
    icd10_map = icd10_map.sort_values(by='icd9')
    
    icd10_map['Description'] = icd10_map.apply(processicd10desc, 1)
    
    return icd10_map

def getICD10withHierarchy(icd10_map, icd10_hier):
        return pd.merge(icd10_map, icd10_hier, left_on='icd10children2', right_on='icd10children2', how='left')

def getICD10withCCSR(icd10_map, icd10_ccsr):
        return pd.merge(icd10_map, icd10_ccsr, left_on='icd10', right_on="'ICD-10-CM CODE'", how='left')
    
if __name__ == '__main__':
    gem_zip_name = './static/diagnosis_gems_2018.zip'
    gem_file = '2018_I9gem.txt'
    unzipFile(gem_zip_name, gem_file)
    
    desc_zip_name = './static/icd10cm_codes_addenda_2019.zip'
    desc_file = 'icd10cm_codes_2019.txt'
    unzipFile(desc_zip_name, desc_file)
    
    icd10_gems = readICD10GEMS(gem_file)
    icd10_desc = readICD10Desc(desc_file)
    
    icd10_mst = pd.merge(icd10_gems, icd10_desc, left_on='icd10', right_on='icd10', how='left')

    icd10_map = fillNAICD10Desc(icd10_mst)    
    icd10_map_copy = icd10_map.copy()
    
    hierarchy_ = True
    if hierarchy_ == True:
        hier_loc = './static/ICD10hierarchy.csv'
        unzipFile(gem_zip_name, gem_file)
        icd10_hier = readICD10Hierarchy(hier_loc)
        icd10_map_copy['icd10children2'] = icd10_map_copy['icd10'].apply(lambda x: x[:3])
        icd10_map_hierarchy = getICD10withHierarchy(icd10_map_copy, icd10_hier)
    
    ccsr_ = True
    if ccsr_ == True:
        ccsr_zip_loc = './static/DXCCSR2019_1.zip'
        ccsr_file = '$DXCCSR2019_1.CSV'
        unzipFile(ccsr_zip_loc, ccsr_file)
        icd10_ccsr = readICD10CCSR(ccsr_file)
        icd10_map_ccsr = getICD10withCCSR(icd10_map_copy, icd10_ccsr)