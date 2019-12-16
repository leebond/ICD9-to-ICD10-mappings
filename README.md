# ICD9-to-ICD10-mappings

There are some hospital legacy systems that continue to codify ICD diagnosis codes into older versions and this causes issues when making analysis between cross-system analysis between legacy and new systems. Data analysts and data scientists will attempt to convert ICD codes between versions but they will require some effort to look into how existing GEMs can be applied.

This repository provides a quick way to convert ICD 9 CM to ICD 10 CM and further extends ICD 10 CM into their hierarchy order as well as CCSR categories; they are organized across 21 body systems, which generally follow the structure of the ICD-10-CM diagnosis chapters (https://www.hcup-us.ahrq.gov/toolssoftware/ccsr/ccs_refined.jsp)
