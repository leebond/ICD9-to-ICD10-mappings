# ICD9-to-ICD10-mappings

There are some hospital legacy systems that continue to codify ICD diagnosis codes into older versions and this causes issues when conducting cross-system analysis between legacy and new systems. Data analysts and data scientists will attempt to convert ICD codes between versions but they will require some effort to look into how conversion can be done and may not be using the right source. 

This repository provides a quick way to convert ICD 9 CM to ICD 10 CM using GEMs (cms.gov) and further extends ICD 10 CM into their hierarchy order as well as CCSR categories (the categories are organized across 21 body systems, which generally follow the structure of the ICD-10-CM diagnosis chapters (https://www.hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp)
