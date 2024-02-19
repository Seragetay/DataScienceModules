# IMPLEMENT A METHOD TO PULL THE TOP THREE MESSAGES
# JOIN MEMBER COVERAGE AND MEMBERSHIP DATAFRAME


import pandas as pd
import os
import duckdb
import pyodbc
import re
import win32com.client as win32
import numpy as np
from datetime import datetime, timedelta, date
import shutil
import glob
import numpy as np
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

# Import incentive file, member coverage
incet_data = pd.read_excel(r"W:\STARS_2024\Stars Team\Akshay\PO Incentive\Q12024POIncentive_20240214.xlsx")
cov_data = pd.read_csv(r"C:\Users\E740616\OneDrive - Blue Cross Blue Shield of Michigan\Documents\Projects\Mem_cov\Mem_coverage.csv")
conn = duckdb.connect(r'C:\Users\E740616\Blue Cross Blue Shield of Michigan\StarsTeam-EH - General\5. Star Data and Important Docs\Stars Analytics\Database\pharmacy_data.db')
#kpi = conn.sql('SELECT  * FROM rx_ante.KPI').df()
rxAnt_ptList = conn.sql('SELECT  * FROM rx_ante.rxante_patient_list').df()
conn.execute("SHOW ALL TABLES").df()
hmo_data = pd.read_excel("BCNA Attribution.xlsx")
seg_col = ["contract_number","market_segment"]
segment = cov_data[seg_col].copy()
trust_data = segment[segment["market_segment"]=="URMBT"].copy()
# MEMBER INFO COMES FROM BELOW CODE

######## PPO file ########


def find_member_address_files(root_folder, file_ext, contains):    
    latest_file = None
    latest_create_time = 0
    for filename in os.listdir(root_folder):
        if filename.endswith(file_ext) and contains in filename and "~$" not in filename:
            file_path = os.path.join(root_folder, filename)
            create_time = os.path.getctime(file_path)
            if create_time > latest_create_time:
                latest_create_time = create_time
                latest_file = file_path
    return latest_file


# Loading membership files

######## PPO file ########


def find_member_address_files(root_folder, file_ext, contains):    
    latest_file = None
    latest_create_time = 0
    for filename in os.listdir(root_folder):
        if filename.endswith(file_ext) and contains in filename and "~$" not in filename:
            file_path = os.path.join(root_folder, filename)
            create_time = os.path.getctime(file_path)
            if create_time > latest_create_time:
                latest_create_time = create_time
                latest_file = file_path
    return latest_file


member_address_root = r'W:\Rx_Ante\Outbound'
latest_mem_add_ppo_files =  find_member_address_files(member_address_root, ".txt", "enrollment")
print(f' Loading....{latest_mem_add_ppo_files}')

######## HMO File ############

latest_mem_add_hmo_files =  find_member_address_files(member_address_root, ".txt", "Enrollment_BCN")
print(f' Loading....{latest_mem_add_hmo_files}')

mem_add_ppo_df = pd.read_csv(latest_mem_add_ppo_files, sep='|')
mem_add_hmo_df = pd.read_csv(latest_mem_add_hmo_files, sep='|')

mem_add_df = pd.concat([mem_add_ppo_df, mem_add_hmo_df], sort = False)
mem_add_df = mem_add_df[['Member_ID','End_Date','Hic_Number','Member_Address_1',	'Member_Address_2',	'Member_City','Member_State',	'Member_Zip_Code',	'Member_Country_Code',	'Member_Eligibility_Phone_Number', 	'Member_Phone_Number',	'Member_Preferred_Phone_Number','Member_Alt1_Phone_Number',	'Member_Alt2_Phone_Number','Member_Alt3_Phone_Number', 'Member_Alt4_Phone_Number', 'Member_Language_Preference']]

mem_add_df.head(10)
mem_add_df.dtypes

mem_add_df['End_Date'] = pd.to_datetime(mem_add_df['End_Date'])

latest_indices = mem_add_df.groupby('Member_ID')['End_Date'].idxmax()
mem_add_df_latest = mem_add_df.loc[latest_indices].reset_index()

mem_add_df_latest['Member_ID'] = mem_add_df_latest['Member_ID'].astype(str).str.strip()
mem_add_df_latest['Member_ID'] = mem_add_df_latest['Member_ID'].str.rstrip('.0')

# Final Membership df
mem_add_df_latest.drop_duplicates(subset='Member_ID', keep='last', inplace = True)

######################## PPO PCP Attribution #####################################
sever_name = 'pwv01441'
database_name = 'CPDM_II'
conn_str = f'DRIVER={{SQL SERVER}};SERVER={sever_name}; DATABASE={database_name};Trusted_connection=yes;'
conn = pyodbc.connect(conn_str)
if conn:
    print("Connection Established successfully... ")

query_str = """
Select Distinct
Person_Sk
,PersonFirstName
,PersonlastName
,SubscriberFirstName
,SubscriberLastName
,Rel_CD
,ContractNum
,PersonGender
,PersonBirthDate
,PersonZip_CD
,PO_ID
,OrgTitle
,SubPO_ID
,SubGroup
,PU_ID
,PracticeUnit
,Practitioner_SK
,PractitionerFirstName
,PractitionerLastName
,BCBSMLicense
,NPI
,PractitionerZip
,PCMH_IND


from CPDM_II.CareRelation.CR_PCPRelationshipSummary
where CR_ID=202401 -- Update it as per the requirements
AND MedMemMths > 0 
--AND PO_ID<>'P99'
AND Population_CD='MAPPO';

"""
ppo_pcp_data = pd.read_sql(query_str, conn)



# Copy datas to dataframes
incet_df = incet_data.copy()
cov_df = cov_data.copy()
rxAnt_pl_df = rxAnt_ptList.copy()
rxAnt_df = rxAnt_pl_df[rxAnt_pl_df['FileName'] == 'RxAnte_patient_list_20240214.xlsx'].copy() # Change it every month
hmo_pcp_df = hmo_data.copy() # HMO PCP Attribution
ppo_pcp_df = ppo_pcp_data.copy() # PPO PCP Attribution
membership_df = mem_add_df_latest.copy()
tust_df = trust_data.copy()

# Covert file_date to datetime
rxAnt_pl_df['file_date'] = pd.to_datetime(rxAnt_pl_df['file_date'], format='%Y%m')
rxAnt_df["FileName"].unique()
######################## Inclusion Criteria ########################################
# Keep PPO and HMO contracts
rxAnt_df["Contract ID"].unique()
incet_df["Contract ID"].unique()

# rxAnt_df["Contract ID"]= rxAnt_df["Contract ID"].str.strip()
# rxAnt_df["Contract ID"] = rxAnt_df[rxAnt_df["Contract ID"].isin(['H9572', 'H5883'])].copy()
# incet_df["Contract ID"] = incet_df[incet_df["Contract ID"].isin(['H9572', 'H5883'])].copy()

######################## Adding Gap days to RxAnti #################################

def add_gapdays_columns(dataframe, column_prefix, column_prefix_alias):
    ''' Add a group of columns related to gap days'''
    dataframe[f"{column_prefix}Index Date"] = pd.to_datetime(dataframe[f"{column_prefix}Index Date"], errors= 'coerce')
    end_of_year = pd.to_datetime(dataframe[f"{column_prefix}Index Date"].dt.year,format = '%Y') + pd.offsets.YearEnd(0)
    dataframe[f'{column_prefix_alias} Allowed gap days'] =round(end_of_year.sub(dataframe[f"{column_prefix}Index Date"]).dt.days*0.2,0) 
    dataframe[f'{column_prefix_alias} Gap Days Incurred'] = dataframe['file_date'].sub(dataframe[f"{column_prefix}Index Date"]).dt.days * (1- pd.to_numeric(dataframe[f'{column_prefix}PDC (YTD)'],errors='coerce'))
    dataframe[f'{column_prefix_alias} Gap Days remaining'] = dataframe[f'{column_prefix_alias} Allowed gap days'] - dataframe[f'{column_prefix_alias} Gap Days Incurred']
    dataframe[f'{column_prefix_alias} percent Gap days remaining'] = dataframe[f'{column_prefix_alias} Gap Days remaining']/ dataframe[f'{column_prefix_alias} Allowed gap days']
    return dataframe

RxAnti_df_gap_days = add_gapdays_columns(rxAnt_df, 'Diabetes Medications_', 'Diab')
RxAnti_df_gap_days = add_gapdays_columns(rxAnt_df, 'RASA_', 'RAS')
RxAnti_df_gap_days = add_gapdays_columns(rxAnt_df, 'Statins_', 'Statin')


print("Gap days added")
#RxAnti_df_gap_days.to_excel("RxAnti_sample.xlsx", index=False)
#membership_df.head(1000).to_excel("Membership_sample.xlsx", index=False)

######################## Exclusion Criteria ########################################
# If member is in the Statin measure only, do not include them on the monthly PO incentive lists
Rx_anti_f_df =RxAnti_df_gap_days.copy()
Rx_anti_f_df = RxAnti_df_gap_days[RxAnti_df_gap_days['Diabetes Medications_Index Date'].notna() | RxAnti_df_gap_days['RASA_Index Date'].notna()].copy()

################################## Combine PCP attribution for HMO and PPO ############################
# WAITING FOR HMO ACCESS 
hmo_pcp_df["PCP NAME"] = hmo_pcp_df["PCP_PRV_FIRST_NM"] + ' ' + hmo_pcp_df["PCP_PRV_LAST_NM"]
hmo_pcp_df["PCP NAME"]
master_attribution = ppo_pcp_df.copy()

master_attribution["PCP NAME"] = master_attribution["PractitionerFirstName"] + ' ' + master_attribution["PractitionerLastName"]

# attribution_cols = ["ContractNum","NPI","OrgTitle","PCP NAME","PO_ID","PU_ID","PracticeUnit","SubGroup", "SubPO_ID"]
hmo_pcp_df["SubGroup"] = ""
hmo_pcp_df["SubPO_ID"] = ""


hmo_pcp_attr_col = ["CONTRACT_MBR", "NPI", "ipa_desc", "PCP NAME", "PCP_PRV_ID", "IPA_CD", "GRP_NM", "SubGroup", "SubPO_ID"]
hmo_pcp_df = hmo_pcp_df[hmo_pcp_attr_col]
hmo_pcp_df.rename(columns={"CONTRACT_MBR": "ContractNum",
                            "IPA_CD": "PO_ID",
                            "PULL_ID": "PU_ID",
                            "ipa_desc": "OrgTitle",
                            "GRP_NM": "PracticeUnit"}, inplace=True)
hmo_pcp_attr_col
#master_attribution
# attribution = master_attribution[hmo_pcp_attr_col].copy()
############################################## Integrating Full risk member ##################################
print("Adding full risk provider information from member roaster")


def find_latest_roster_files(root_folder):
    # Create a list to store the matching file paths
    matching_files = []
    
    # Traverse through all subfolders and files in the root folder
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # Check if the file is an Excel file (.xlsx) and contains "patient_list" in the name
            if file.endswith(".csv") and "Roster" in file and "~$" not in file :
                # Build the absolute file path
                file_path = os.path.join(root, file)
                
                # Add the file path to the matching_files list
                matching_files.append(file_path)
    
    return matching_files

roster_root = r'\\Det_Gen01\CoEStars\Data Drop\Outgoing_Reports\Member_Roster'
member_roster_files =  find_latest_roster_files(roster_root)
print(member_roster_files)

latest_roster_file = member_roster_files[-1]
print(f' Loading....{latest_roster_file}')

member_roster_df = pd.read_csv(latest_roster_file, sep='|')
member_roster_df.head()
member_roster_df = member_roster_df[member_roster_df['outcome_type'] == 'Primary']
member_roster_df.columns
member_roster_mini_cols = ['contract_number','risk_program_level_name', 'outcome_type','medicare_beneficiary_identifier',  'program_code', 'program_name', 'primary_care_provider_national_provider_identifier','primary_care_provider_name', 'primary_care_provider_group_name']
member_roster_mini_df = member_roster_df[member_roster_df.columns.intersection(member_roster_mini_cols)] 
mfulRsk_cols = ['contract_number', 'risk_program_level_name', 'medicare_beneficiary_identifier']
meaningingFullRisk = member_roster_mini_df[mfulRsk_cols].copy()
meaningingFullRisk.head(2)
################################ Filter Needed columns ###############################################

rxnt_cols = ["Member Id","Contract ID","Member First Name","Member Last Name","Member Date of Birth",
             "Diabetes Medications_Futile Date","RASA_Futile Date","Statins_Futile Date",
             "Diabetes Medications_Index Date",
             "Diabetes Medications_Most Recent Rx","Diabetes Medications_NDC",
             "Diabetes Medications_Most Recent Fill Date","Diabetes Medications_Next Fill Due Date",
             "Diabetes Medications_Pharmacy NPI","Diabetes Medications_Pharmacy Name",
             "Diabetes Medications_Pharmacy Phone","Diabetes Medications_Prescriber NPI",
             "Diabetes Medications_Days Supply to Adherent","Diabetes Medications_PDC (YTD)",
             "Diabetes Medications_Current Fill Status","Diabetes Medications_Fill Count (YTD)",
             "RASA_Index Date","RASA_Most Recent Rx","RASA_NDC",
             "RASA_Most Recent Fill Date","RASA_Next Fill Due Date","RASA_Pharmacy NPI",
             "RASA_Pharmacy Name","RASA_Pharmacy Phone","RASA_Prescriber NPI",
             "RASA_Days Supply to Adherent","RASA_PDC (YTD)","RASA_Current Fill Status",
             "RASA_Fill Count (YTD)","Statins_Index Date",
             "Statins_Most Recent Rx","Statins_NDC","Statins_Most Recent Fill Date",
             "Statins_Next Fill Due Date","Statins_Pharmacy NPI","Statins_Pharmacy Name",
             "Statins_Pharmacy Phone","Statins_Prescriber NPI","Statins_Days Supply to Adherent",
             "Statins_PDC (YTD)","Statins_Current Fill Status","Statins_Fill Count (YTD)",
             "Diab Gap Days remaining","RAS Gap Days remaining","Statin Gap Days remaining","FileName"]

#,"Diabetes Medications_New to Therapy" ,"RASA_New to Therapy" "Statins_New to Therapy",

rxAnti = Rx_anti_f_df[rxnt_cols].copy()
rxAnti["Contract ID"]
attribution_cols = ["ContractNum","NPI","OrgTitle","PCP NAME","PO_ID","PU_ID","PracticeUnit","SubGroup",
                    "SubPO_ID"]




attribution = master_attribution[attribution_cols].copy()
attribution = pd.concat([attribution, hmo_pcp_df])

incetive_cols = ["Member ID","Diabetes Med Refills Remaining","Diabetes Med Day Supply","RASA Med Refills Remaining",
                "RASA Med Day Supply","Statins Med Refills Remaining","Statins Med Day Supply"]

incentive = incet_df[incetive_cols].copy()


membership_cols =["Member_ID","Hic_Number","Member_Phone_Number","Member_Alt1_Phone_Number","Member_Alt2_Phone_Number",
                  "Member_Alt3_Phone_Number","Member_Alt4_Phone_Number","Member_Eligibility_Phone_Number",
                  "Member_Language_Preference","Member_Address_1","Member_Address_2","Member_City",
                  "Member_State","Member_Zip_Code","Member_Country_Code"]

membership_df = membership_df[membership_cols].copy()


###################################
rxAnti["Member Id"] = rxAnti["Member Id"].str.strip()
incentive["Member ID"] = incentive["Member ID"].str.strip()
attribution["ContractNum"] = attribution["ContractNum"].str.strip()
membership_df["Member_ID"]= membership_df["Member_ID"].str.strip()


df1 = rxAnti.merge(incentive, left_on="Member Id", right_on="Member ID", how="left")
df1 = df1.drop("Member ID", axis=1)

df2 = df1.merge(attribution, left_on="Member Id", right_on="ContractNum", how="left")
df2 = df2.drop("ContractNum", axis=1)

final_master_df_1 = df2.merge(membership_df, left_on="Member Id", right_on="Member_ID", how="left")
final_master_df_1 = final_master_df_1.drop("Member_ID", axis=1)


final_master_df = final_master_df_1.merge(meaningingFullRisk, left_on="Member Id", right_on="contract_number", how="left")

final_master_df = final_master_df.drop("contract_number", axis=1)
final_master_df = final_master_df.drop("medicare_beneficiary_identifier", axis=1)


meaningingFullRisk.head(2)


final_master_df["Diabetes action 1"] = ""
final_master_df["Diabetes action 2"] = ""
final_master_df["Diabetes action 3"] = ""
final_master_df["RASA action 1"] = ""
final_master_df["RASA action 2"] = ""
final_master_df["RASA action 3"] = ""
final_master_df["Statins action 1"] = ""
final_master_df["Statins action 2"] = ""
final_master_df["Statins action 3"] = ""

# Add Hic 



################################### Re-arranging columns ##################################################
required_order = ["Member Id","Contract ID","Member First Name","Member Last Name","Member Date of Birth",
"Hic_Number","Diabetes action 1","Diabetes action 2","Diabetes action 3","Diabetes Medications_Futile Date",
"RASA action 1","RASA action 2","RASA action 3","RASA_Futile Date","Statins action 1","Statins action 2",
"Statins action 3","Statins_Futile Date","Member_Phone_Number","Member_Alt1_Phone_Number","Member_Alt2_Phone_Number",
"Member_Alt3_Phone_Number","Member_Alt4_Phone_Number","Member_Eligibility_Phone_Number","Member_Language_Preference",
"Member_Address_1","Member_Address_2","Member_City","Member_State","Member_Zip_Code","Member_Country_Code","NPI",
"OrgTitle","PCP NAME","PO_ID","PU_ID","PracticeUnit","SubGroup","SubPO_ID",
"Diabetes Medications_Index Date","Diabetes Medications_Most Recent Rx",
"Diabetes Medications_NDC","Diabetes Medications_Most Recent Fill Date","Diabetes Medications_Next Fill Due Date",
"Diabetes Medications_Pharmacy NPI","Diabetes Medications_Pharmacy Name","Diabetes Medications_Pharmacy Phone",
"Diabetes Medications_Prescriber NPI","Diabetes Medications_Days Supply to Adherent","Diabetes Medications_PDC (YTD)",
"Diabetes Medications_Current Fill Status","Diabetes Med Refills Remaining","Diabetes Med Day Supply",
"Diabetes Medications_Fill Count (YTD)","RASA_Index Date","RASA_Most Recent Rx","RASA_NDC",
"RASA_Most Recent Fill Date","RASA_Next Fill Due Date","RASA_Pharmacy NPI","RASA_Pharmacy Name","RASA_Pharmacy Phone",
"RASA_Prescriber NPI","RASA_Days Supply to Adherent","RASA_PDC (YTD)","RASA_Current Fill Status",
"RASA Med Refills Remaining","RASA Med Day Supply","RASA_Fill Count (YTD)","Statins_Index Date",
"Statins_Most Recent Rx","Statins_NDC","Statins_Most Recent Fill Date",
"Statins_Next Fill Due Date","Statins_Pharmacy NPI","Statins_Pharmacy Name","Statins_Pharmacy Phone",
"Statins_Prescriber NPI","Statins_Days Supply to Adherent","Statins_PDC (YTD)","Statins_Current Fill Status",
"Statins Med Refills Remaining","Statins Med Day Supply","Statins_Fill Count (YTD)","Diab Gap Days remaining",
"RAS Gap Days remaining","Statin Gap Days remaining","FileName","risk_program_level_name"]
#,"RASA_New to Therapy" "Statins_New to Therapy", ,"Diabetes Medications_New to Therapy"

final_master_df = final_master_df[required_order]
#final_master_df["Hic_Number"].to_excel("HIC.xlsx", index=False)
################################### Re-Name columns #######################################################

final_master_df.rename(columns={'Diabetes Medications_Futile Date': 'Diabetes Medications_Non-recoverable date',
                                'RASA_Futile Date': 'RASA_Non-recoverable date',
                                'Statins_Futile Date': 'Statins_Non-recoverable date',
                                'Member_Phone_Number': 'Member_Preferred_Phone_Number',
                                'FileName': 'file_name_prefix',
                                'risk_program_level_name': 'Meaningful_risk_Ind'}, inplace=True)




# final_master_df.to_excel("FINAL_TEST.xlsx", index=False)
# final_master_df.head(1000).to_excel("Sample_file.xlsx", index=False)
# rxAnt_ptList.to_excel("MEMBER_LIST.xlsx", index=False)
# final_master_df.to_excel(r"W:\STARS_2024\Stars Team\Akshay\PO Incentive\First_draft.xlsx", index=False)

#################################### Apply The logic ######################################################
# Messages logic

                           ######## Diabetes Logics ##########
#Using Vickis weekly list, if column I (Diabetes Medications_2023 NonAdh)=1 or column K 
# (Diabetes medications_early gap days 2023)=1 and column V(Diabetes Med Day Supply) <84ds, populate “90d Conversion” 

logic_inc_df = final_master_df.copy()
select_cols_1 = ["Member ID", "Diabetes Medications_2023 NonAdh", "Diabetes Medications_Early Gap Days 2023", "Diabetes Med Day Supply",
                 "Diabetes Medications_Pharmacy_Preferred_Standard", "Diabetes Medications_Pharmacy_MO_Retail", "Coverage Gap Stage",
                 "Group_Individual_Plan", "Diabetes Medications_Tier", "Diabetes Medications_Brand Only", "Diabetes Medications_NTT",
                 "Diabetes Med Refills Remaining", "RASA_2023 NonAdh", "RASA_Early Gap Days 2023", "RASA Med Day Supply",
                 "RASA_Pharmacy_MO_Retail", "RASA Med Refills Remaining", "RASA_NTT", "RASA_Pharmacy_Preferred_Standard",
                 "Statins_2023 NonAdh", "Statins_Early Gap Days 2023", "Statins Med Day Supply", "Statins_Pharmacy_Preferred_Standard",
                 "Statins Med Refills Remaining", "Statins_NTT", "Statins_Pharmacy_MO_Retail"]

incent_1 = incet_data[select_cols_1].copy()

incent_1.rename(columns={"Diabetes Medications_2023 NonAdh": "Diabetes Medications_2023 NonAdh_c",
                         "Diabetes Medications_Early Gap Days 2023": "Diabetes Medications_Early Gap Days 2023_c",
                         "Diabetes Med Day Supply": "Diabetes Med Day Supply_c",
                         "Diabetes Med Refills Remaining": "Diabetes Med Refills Remaining_c",
                         "RASA_2023 NonAdh": "RASA_2023 NonAdh_c",
                         "RASA_Early Gap Days 2023": "RASA_Early Gap Days 2023_c",
                         "RASA Med Day Supply": "RASA Med Day Supply_c",
                         "RASA Med Refills Remaining": "RASA Med Refills Remaining_c",
                         "Statins_2023 NonAdh": "Statins_2023 NonAdh_c",
                         "Statins_Early Gap Days 2023": "Statins_Early Gap Days 2023_c",
                         "Statins Med Day Supply": "Statins Med Day Supply_c",
                         "Statins Med Refills Remaining": "Statins Med Refills Remaining_c",
                         "Statins_Pharmacy_MO_Retail": "Statins_Pharmacy_MO_Retail_c"}, inplace=True)

log_1 = logic_inc_df.merge(incent_1, left_on="Member Id", right_on="Member ID", how="left")

log_1["Diabetes action 4"] = ""
log_1["Diabetes action 5"] = ""
log_1["Diabetes action 6"] = ""
log_1["Diabetes action 7"] = ""
log_1["RASA action 4"] = ""
log_1["RASA action 5"] = ""
log_1["Statins action 4"] = ""
log_1["Statins action 5"] = ""




log_1["Diabetes Med Refills Remaining_c"]


log_1["Diabetes Med Day Supply_c"] = pd.to_numeric(log_1["Diabetes Med Day Supply_c"], errors='coerce')
log_1["Diabetes Medications_2023 NonAdh_c"] = pd.to_numeric(log_1["Diabetes Medications_2023 NonAdh_c"], errors='coerce')
log_1["Diabetes Medications_Early Gap Days 2023_c"] = pd.to_numeric(log_1["Diabetes Medications_Early Gap Days 2023_c"], errors='coerce')
log_1["Diabetes Medications_Brand Only"] = pd.to_numeric(log_1["Diabetes Medications_Brand Only"], errors='coerce')
log_1["Diabetes Medications_Tier"] = pd.to_numeric(log_1["Diabetes Medications_Tier"], errors='coerce')
log_1["Diabetes Medications_NTT"] = pd.to_numeric(log_1["Diabetes Medications_NTT"], errors='coerce')
log_1["Diabetes Med Refills Remaining_c"] = pd.to_numeric(log_1["Diabetes Med Refills Remaining_c"], errors='coerce')
log_1["RASA_2023 NonAdh_c"] = pd.to_numeric(log_1["RASA_2023 NonAdh_c"], errors='coerce')
log_1["RASA_Early Gap Days 2023_c"] = pd.to_numeric(log_1["RASA_Early Gap Days 2023_c"], errors='coerce')
log_1["RASA Med Refills Remaining_c"] = pd.to_numeric(log_1["RASA Med Refills Remaining_c"], errors='coerce')
log_1["RASA_NTT"] = pd.to_numeric(log_1["RASA_NTT"], errors='coerce')
log_1["Statins_2023 NonAdh_c"] = pd.to_numeric(log_1["Statins_2023 NonAdh_c"], errors='coerce')
log_1["Statins_Early Gap Days 2023_c"] = pd.to_numeric(log_1["Statins_Early Gap Days 2023_c"], errors='coerce')
log_1["Statins Med Day Supply_c"] = pd.to_numeric(log_1["Statins Med Day Supply_c"], errors='coerce')
log_1["RASA Med Day Supply_c"] = pd.to_numeric(log_1["RASA Med Day Supply_c"], errors='coerce')





 ######################### Suggusted solution ######################################################

log_1["Diabetes action 7"] = np.where(((log_1["Diabetes Medications_2023 NonAdh_c"]== 1) | (log_1["Diabetes Medications_Early Gap Days 2023_c"]== 1)) & (log_1["Diabetes Med Day Supply_c"] < 84), '90d Conversion', log_1["Diabetes action 7"])
# Updated to & log_1["Diabetes Medications_Pharmacy_MO_Retail"] == 'Not Mail Order'
log_1["Diabetes action 6"] = np.where(((log_1["Diabetes Medications_2023 NonAdh_c"]== 1) | (log_1["Diabetes Medications_Early Gap Days 2023_c"]== 1)) & ((log_1["Diabetes Medications_Pharmacy_Preferred_Standard"] == 'Standard') & (log_1["Diabetes Medications_Pharmacy_MO_Retail"] == 'Not Mail Order')), 'Standard to Preferred Pharmacy', log_1["Diabetes action 6"])
log_1["Diabetes action 5"] = np.where(((log_1["Diabetes Medications_2023 NonAdh_c"]== 1) | (log_1["Diabetes Medications_Early Gap Days 2023_c"]== 1)) & (log_1["Diabetes Medications_Pharmacy_MO_Retail"] == 'Not Mail Order'), 'Retail to Mail Order Pharmacy', log_1["Diabetes action 5"])
log_1["Diabetes action 2"] = np.where((log_1["Coverage Gap Stage"]== "INITIAL COVERAGE") & (log_1["Group_Individual_Plan"]== "Individual") & (log_1["Diabetes Medications_Tier"] == 3) & (log_1["Diabetes Medications_Pharmacy_MO_Retail"] == 'Not Mail Order'), 'Cost Savings at Mail order Pharmacy', log_1["Diabetes action 2"])
#Using Vickis weekly list, if , Column I(Diabetes Medications_2023 NonAdh)=1 or column K (diabetes_medications_early gap days 2023)=1 
# and column O (diabetes medications_brand only), populate "Consider Generic"
log_1["Diabetes action 4"] = np.where(((log_1["Diabetes Medications_2023 NonAdh_c"]== 1) | (log_1["Diabetes Medications_Early Gap Days 2023_c"]== 1)) & (log_1["Diabetes Medications_Brand Only"] == 1), 'Consider Generic', log_1["Diabetes action 4"])
log_1["Diabetes action 1"] = np.where((log_1["Diabetes Medications_NTT"] == 1), 'New to Therapy', log_1["Diabetes action 1"])
log_1["Diabetes action 3"] = np.where((log_1["Diabetes Med Refills Remaining_c"].isin([0,1])), '0 to 1 Refill Remaining', log_1["Diabetes action 3"])

                           ######## RASA Logics ##########

#Using Vickis weekly list, if column W(RASA_2023 NonAdh)=1 or column Y (RASA_Early Gap Days 2023)=1 
# and column AH (RASA Med Day Supply)<84ds, populate “90d Conversion”

log_1["RASA action 5"] = np.where(((log_1["RASA_2023 NonAdh_c"]== 1) | (log_1["RASA_Early Gap Days 2023_c"]== 1)) & (log_1["RASA Med Day Supply_c"] < 84), '90d Conversion', log_1["RASA action 5"])

#Using Vickis weekly list, if column W (RASA_2023 NonAdh)=1 or column Y (RASA_Early Gap Days 2023)=1 and column 
# AF(RASA_Pharmacy_Preferred_Standard)= Standard, populate “Standard to Preferred Pharmacy” 
# NOTE: exclude the Trust membership from this category

log_1["RASA action 4"] = np.where(((log_1["RASA_2023 NonAdh_c"]== 1) | (log_1["RASA_Early Gap Days 2023_c"]== 1)) & ((log_1["RASA_Pharmacy_Preferred_Standard"] == 'Standard') & (log_1["RASA_Pharmacy_MO_Retail"] == 'Not Mail Order')), 'Standard to Preferred Pharmacy', log_1["RASA action 4"])

#Using Vickis weekly list, if column W (RASA_2023 NonAdh)= 1 or column Y (RASA_Early Gap Days 2023)=1 
# and Column AE(RASA_Pharmacy_MO_Retail)= Not Mail Order populate “Retail to Mail Order Pharmacy” 

log_1["RASA action 3"] = np.where(((log_1["RASA_2023 NonAdh_c"]== 1) | (log_1["RASA_Early Gap Days 2023_c"]== 1)) & (log_1["RASA_Pharmacy_MO_Retail"] == 'Not Mail Order'), 'Retail to Mail Order Pharmacy', log_1["RASA action 3"])

#Using Vickis weekly list, if column AG=0 or 1, populate "No Refills Remaining"

log_1["RASA action 2"] = np.where((log_1["RASA Med Refills Remaining_c"].isin([0,1])), '0 to 1 Refill Remaining', log_1["RASA action 2"])

# Using Vickis weekly list, if column X (RASA_NTT)= 1, populate "New to Therapy"

log_1["RASA action 1"] = np.where((log_1["RASA_NTT"] == 1), 'New to Therapy', log_1["RASA action 1"])




                           ######## RASA Logics ##########
#o   Using Vickis weekly list, if column AI (Statins_2023 NonAdh)=1 or column AK (Statins_Early Gap Days 2023)=1 
# and column AT= (Statin Med Day Supply)<84ds, populate “90d Conversion” 

log_1["Statins action 5"] = np.where(((log_1["Statins_2023 NonAdh_c"]== 1) | (log_1["Statins_Early Gap Days 2023_c"]== 1)) & (log_1["Statins Med Day Supply_c"] < 84), '90d Conversion', log_1["Statins action 5"])

#Using Vickis weekly list, if column AI (Statins_2023 NonAdh)=1 or column AK(Statins_Early Gap Days 2023)=1  
# and column AR(Statins_Pharmacy_Preferred_Standard)= Standard, populate “Standard to Preferred Pharmacy” 
# NOTE: exclude the Trust membership from this category
# Updated to (log_1["Statins_Pharmacy_MO_Retail_c"] == 'Not Mail Order')
log_1["Statins action 4"] = np.where(((log_1["Statins_2023 NonAdh_c"]== 1) | (log_1["Statins_Early Gap Days 2023_c"]== 1)) & ((log_1["Statins_Pharmacy_Preferred_Standard"] == 'Standard') & (log_1["Statins_Pharmacy_MO_Retail_c"] == 'Not Mail Order')), 'Standard to Preferred Pharmacy', log_1["Statins action 4"])

#Using Vickis weekly list, if column AI (Statins_2023 NonAdh)= 1 or column AK (Statins_Early Gap Days 2023)=1 
# and Column AQ (Statins_Pharmacy_MO_Retail)= Not Mail Order, populate “Retail to Mail Order Pharmacy” 

log_1["Statins action 3"] = np.where(((log_1["Statins_2023 NonAdh_c"]== 1) | (log_1["Statins_Early Gap Days 2023_c"]== 1)) & (log_1["Statins_Pharmacy_MO_Retail_c"] == 'Not Mail Order'), 'Retail to Mail Order Pharmacy', log_1["Statins action 3"])

#Using Vickis weekly list, if column AS=0 or 1, populate "No Refills Remaining"

log_1["Statins action 2"] = np.where((log_1["Statins Med Refills Remaining_c"].isin([0,1])), '0 to 1 Refill Remaining', log_1["Statins action 2"])

#Using Vickis weekly list, if column AJ (Statins_NTT)= 1, populate "New to Therapy"

log_1["Statins action 1"] = np.where((log_1["Statins_NTT"] == 1), 'New to Therapy', log_1["Statins action 1"])




##### DROP Extra columns ##########
final_df = log_1.copy()

select_cols_drop = ["Diabetes Medications_2023 NonAdh_c","Diabetes Medications_Early Gap Days 2023_c",
                    "Diabetes Med Day Supply_c","Diabetes Medications_Pharmacy_Preferred_Standard",
                    "Diabetes Medications_Pharmacy_MO_Retail","Coverage Gap Stage","Group_Individual_Plan",
                    "Diabetes Medications_Tier","Diabetes Medications_Brand Only","Diabetes Medications_NTT",
                    "Diabetes Med Refills Remaining_c","RASA_2023 NonAdh_c","RASA_Early Gap Days 2023_c",
                    "RASA Med Day Supply_c","RASA_Pharmacy_MO_Retail","RASA Med Refills Remaining_c","RASA_NTT",
                    "RASA_Pharmacy_Preferred_Standard","Statins_2023 NonAdh_c","Statins_Early Gap Days 2023_c",
                    "Statins Med Day Supply_c","Statins_Pharmacy_Preferred_Standard","Statins Med Refills Remaining_c",
                    "Statins_NTT","Statins_Pharmacy_MO_Retail_c"]

final_df.drop(columns=select_cols_drop, axis=1, inplace=True)




##################### Fill the missing Medicare ID from Member coverage ##################################
cov_df["health_insurance_benefit_medicare_number"] = cov_df["health_insurance_benefit_medicare_number"].str.strip()
log_1["Member Id"] = log_1["Member Id"].str.strip()
mem_cov_selected_cols = ["contract_number", "health_insurance_benefit_medicare_number"]

medicare_ids = cov_df[mem_cov_selected_cols].copy()

final_df = final_df.merge(medicare_ids, left_on="Member Id", right_on="contract_number", how="left")
final_df["Hic_Number"] = final_df["Hic_Number"].fillna(final_df["health_insurance_benefit_medicare_number"])

######### Exclude Trust Members from “Standard to Preferred Pharmacy” Warning ###################
def mask_prefr_trust(df1, df2, action):
    mask = (df1["Member Id"].isin(df2["contract_number"])) & (df1[action] == "Standard to Preferred Pharmacy")
    df1.loc[mask, action] = ''

    return df1

final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 1")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 2")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 3")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 4")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 5")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 6")
final_df = mask_prefr_trust(final_df, tust_df, "Diabetes action 7")

final_df = mask_prefr_trust(final_df, tust_df, "RASA action 1")
final_df = mask_prefr_trust(final_df, tust_df, "RASA action 2")
final_df = mask_prefr_trust(final_df, tust_df, "RASA action 3")
final_df = mask_prefr_trust(final_df, tust_df, "RASA action 4")
final_df = mask_prefr_trust(final_df, tust_df, "RASA action 5")




final_df = mask_prefr_trust(final_df, tust_df, "Statins action 1")
final_df = mask_prefr_trust(final_df, tust_df, "Statins action 2")
final_df = mask_prefr_trust(final_df, tust_df, "Statins action 3")
final_df = mask_prefr_trust(final_df, tust_df, "Statins action 4")
final_df = mask_prefr_trust(final_df, tust_df, "Statins action 5")

final_df = final_df.merge(tust_df, left_on="Member Id", right_on="contract_number", how="left")

########## Final Re-arrage columns #######################

re_arranged_final = ["Member Id","Contract ID","Member First Name","Member Last Name","Member Date of Birth",
                     "Hic_Number","market_segment", "Diabetes action 1","Diabetes action 2","Diabetes action 3","Diabetes action 4",
                     "Diabetes action 5","Diabetes action 6","Diabetes action 7",
                     "Diabetes Medications_Non-recoverable date","RASA action 1","RASA action 2", 
                     "RASA action 3","RASA action 4","RASA action 5", "RASA_Non-recoverable date","Statins action 1",
                     "Statins action 2","Statins action 3","Statins action 4","Statins action 5",
                     "Statins_Non-recoverable date","Member_Preferred_Phone_Number","Member_Alt1_Phone_Number",
                     "Member_Alt2_Phone_Number","Member_Alt3_Phone_Number","Member_Alt4_Phone_Number",
                     "Member_Eligibility_Phone_Number","Member_Language_Preference","Member_Address_1","Member_Address_2",
                     "Member_City","Member_State","Member_Zip_Code","Member_Country_Code","NPI","OrgTitle","PCP NAME",
                     "PO_ID","PU_ID","PracticeUnit","SubGroup","SubPO_ID","Diabetes Medications_Index Date",
                     "Diabetes Medications_Most Recent Rx","Diabetes Medications_NDC",
                     "Diabetes Medications_Most Recent Fill Date","Diabetes Medications_Next Fill Due Date",
                     "Diabetes Medications_Pharmacy NPI","Diabetes Medications_Pharmacy Name",
                     "Diabetes Medications_Pharmacy Phone","Diabetes Medications_Prescriber NPI",
                     "Diabetes Medications_Days Supply to Adherent","Diabetes Medications_PDC (YTD)",
                     "Diabetes Medications_Current Fill Status","Diabetes Med Refills Remaining","Diabetes Med Day Supply",
                     "Diabetes Medications_Fill Count (YTD)","RASA_Index Date","RASA_Most Recent Rx","RASA_NDC",
                     "RASA_Most Recent Fill Date","RASA_Next Fill Due Date","RASA_Pharmacy NPI","RASA_Pharmacy Name",
                     "RASA_Pharmacy Phone","RASA_Prescriber NPI","RASA_Days Supply to Adherent","RASA_PDC (YTD)",
                     "RASA_Current Fill Status","RASA Med Refills Remaining","RASA Med Day Supply","RASA_Fill Count (YTD)",
                     "Statins_Index Date","Statins_Most Recent Rx","Statins_NDC","Statins_Most Recent Fill Date",
                     "Statins_Next Fill Due Date","Statins_Pharmacy NPI","Statins_Pharmacy Name","Statins_Pharmacy Phone",
                     "Statins_Prescriber NPI","Statins_Days Supply to Adherent","Statins_PDC (YTD)",
                     "Statins_Current Fill Status","Statins Med Refills Remaining","Statins Med Day Supply",
                     "Statins_Fill Count (YTD)","Diab Gap Days remaining","RAS Gap Days remaining",
                     "Statin Gap Days remaining","file_name_prefix","Meaningful_risk_Ind"]




final_df = final_df[re_arranged_final]


# Writing the file
final_df.to_excel("Final_Draft__list_20240214.xlsx", index=False)

final_df_PO = final_df.copy()

############### Creating Run folders and files ###############

edifecs_file_location = r"W:\STARS_2023\Stars Team\Akshay\PGIP_MCG Edifecs Mailboxes IDs.xlsx"
pgip_ppo_name = pd.read_excel(edifecs_file_location, sheet_name = 'PGIP (MAPPO) ' )

pgip_hmo_name = pd.read_excel(edifecs_file_location, sheet_name = 'MCG (BCNA)' )

pgip_ppo_name['file_name_prefix'] = pgip_ppo_name['EDDI Mailbox'] + "~" + pgip_ppo_name['Mailbox Name']		
pgip_ppo_name_2 = pgip_ppo_name[['PO ID', 'file_name_prefix']]

pgip_hmo_name['file_name_prefix'] = pgip_hmo_name['Mailbox for all other files'] + "~" + pgip_hmo_name['DS']		

pgip_hmo_name.rename(columns = {'ID': 'PO ID'}, inplace = True)

pgip_hmo_name_2 = pgip_hmo_name[['PO ID', 'file_name_prefix']]

pgip_final_name = pd.concat([pgip_ppo_name_2,pgip_hmo_name_2])

pgip_final_name['PO ID'] = pgip_final_name['PO ID'].astype(str).str.strip() 

pgip_final_name['file_name_prefix'].value_counts()
final_df_PO['PO_ID'] = final_df_PO['PO_ID'].astype(str).str.strip() 


final_df_PO = pd.merge(final_df_PO,pgip_final_name, how = 'left' , left_on='PO_ID', right_on= 'PO ID')

#Create folder by the date of File and export in cvs
root_folder = r"W:\STARS_2024\Stars Team\Akshay\PO Incentive"

def find_patient_list_files(root_folder):
    # Create a list to store the matching file paths
    matching_files = []
    
    # Traverse through all subfolders and files in the root folder
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # Check if the file is an Excel file (.xlsx) and contains "patient_list" in the name
            if file.endswith(".xlsx") and "Final_Draft_02_12" in file and "~$" not in file : #CHANGE THE FILE NAME
                # Build the absolute file path
                file_path = os.path.join(root, file)
                
                # Add the file path to the matching_files list
                matching_files.append(file_path)
    
    return matching_files

# Specify the root folder where the search should start


# Call the function to find the matching files
matching_files = find_patient_list_files(root_folder)
matching_files


file_path = matching_files[-1]
print(f' Loading....{file_path}')
type(file_path)
pattern = r"(.{8})\.xlsx$"
match = re.search(pattern, file_path ) 
extracted_char = match.group(1)
print(f' Loading file date....{extracted_char}')


final_df_PO_final_only_AHA = final_df_PO[final_df_PO['SubGroup'] == 'Accountable Healthcare Advantage']

final_df_PO_final_without_AHA = final_df_PO[final_df_PO['SubGroup'] != 'Accountable Healthcare Advantage']

directory_path = rf'W:\STARS_2024\Stars Team\Akshay\PO Incentive\{extracted_char}'

if os.path.exists(directory_path):
    # Remove all files and subdirectories in the existing directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
else:
    # Create the directory if it doesn't exist
    os.makedirs(directory_path)
final_df_PO_final_without_AHA

grouped = final_df_PO_final_without_AHA.groupby('PO_ID')
grouped

for group_name, group_df in grouped:
    file_name = f"{directory_path}\\{group_df['file_name_prefix_y'].iloc[0]}_{group_name}_{extracted_char}_EOY_Incentive_Target_Lists.csv"
    group_df.to_csv(file_name, index=False)
    print(f"{group_name} {group_df['OrgTitle'].iloc[0]} file create")

