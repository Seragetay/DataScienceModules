////// CAHPS Calc //////

import pandas as pd 
import os
import matplotlib as plt
import openpyxl
#from docx import Document
#from pptx import Presentation
#from pptx.util import Inches



def read_file():
    # Read the file
    file_path = "50207BCBS50207data_all-BCBSH9572PPO.xlsx"
    sheet_name = "BCBS50207 data_all"
    file_data = pd.read_excel(file_path, sheet_name)
    print("File Loaded")
    w_df = file_data[file_data["id_disp"].isin([10, 31])]
    print("Filtered")
    race_filter = ["Black", "Asian", "Hispanic", "North American Native",
                   "Other"]
    non_disability_filter = ["Unknown", "N"] 
    lis_filter = ["Unknown", "N"] # low pop
    #w_df = w_df[w_df["Org_Disability"].isin(["Y"])]
    w_df = w_df[w_df["Race"].isin(race_filter)]

    return w_df

############################################################################
wd = read_file()
wd.Race.unique()
wd.columns
# Assign variables to each category
# Rating_of_Health_Plan question = q38

def single_q(question): # for cat with single question
    valid_col = wd[~wd[question].isin([99, ' '])]
    value = valid_col[question].mean()
    pop = len(valid_col)
    value = ((value - 0) * 100)/(10-0)

    return {"Score":value, "Count":pop}

def care_and_cordnate(question, denm): # for cat with single question
    valid_col = wd[~wd[question].isin([99, ' ', 5, 6])]
    value = valid_col[question].mean()
    pop = len(valid_col)
    value = ((value - 1) * 100)/(denm-1)

    return {"Score":value, "Count":pop}

# Functions to calculate over all scores for each composite questions

def overAllpop_2(q1, q2):

    qOne = wd[~wd[q1].isin([99, " "])] 
    qTwo = wd[~wd[q2].isin([99, " "])] 

    combined = pd.concat([qOne, qTwo])

    combined = combined.drop_duplicates(subset="id_dss")
    overAllpop = combined["id_dss"]
    
    return len(overAllpop)

def overAllpop_3(q1, q2, q3):

    qOne = wd[~wd[q1].isin([99, " "])] 
    qTwo = wd[~wd[q2].isin([99, " "])] 
    qThree = wd[~wd[q3].isin([99, " "])] 

    combined = pd.concat([qOne, qTwo, qThree])

    combined = combined.drop_duplicates(subset="id_dss")
    overAllpop = combined["id_dss"]
    
    return len(overAllpop)

def overAllpop_4(q1, q2, q3, q4):

    qOne = wd[~wd[q1].isin([99, " "])] 
    qTwo = wd[~wd[q2].isin([99, " "])] 
    qThree = wd[~wd[q3].isin([99, " "])]
    qFour = wd[~wd[q4].isin([99, " "])]  

    combined = pd.concat([qOne, qTwo, qThree, qFour])

    combined = combined.drop_duplicates(subset="id_dss")
    overAllpop = combined["id_dss"]
    
    return len(overAllpop)

def overAllpop_5(q1, q2, q3, q4, q5):

    qOne = wd[~wd[q1].isin([99, " "])] 
    qTwo = wd[~wd[q2].isin([99, " "])] 
    qThree = wd[~wd[q3].isin([99, " "])]
    qFour = wd[~wd[q4].isin([99, " "])]  
    qFive = wd[~wd[q5].isin([99, " "])]

    combined = pd.concat([qOne, qTwo, qThree, qFour, qFive])

    combined = combined.drop_duplicates(subset="id_dss")
    overAllpop = combined["id_dss"]
    
    return len(overAllpop)

def overAllpop_6(q1, q2, q3, q4, q5, q6):

    qOne = wd[~wd[q1].isin([99, " "])] 
    qTwo = wd[~wd[q2].isin([99, " "])] 
    qThree = wd[~wd[q3].isin([99, " "])]
    qFour = wd[~wd[q4].isin([99, " "])]  
    qFive = wd[~wd[q5].isin([99, " "])]
    qSix = wd[~wd[q5].isin([99, " "])]

    combined = pd.concat([qOne, qTwo, qThree, qFour, qFive, qSix])

    combined = combined.drop_duplicates(subset="id_dss")
    overAllpop = combined["id_dss"]
    
    return len(overAllpop)




rating_of_Health_Plan = single_q("q38")
rating_of_Health_Care = single_q("q09")
rating_of_drug_plan = single_q('q45')

# Health Plan Customer Service

getting_information_h = care_and_cordnate("q34", 4)
treated_with_courtesy_respect = care_and_cordnate("q35", 4)
health_plan_forms_easy_to_fill_out = care_and_cordnate("Q36_37", 4)

health_plan_customer_service_lst= [getting_information_h["Score"], treated_with_courtesy_respect["Score"], health_plan_forms_easy_to_fill_out["Score"]]
health_plan_customer_service= round(sum(health_plan_customer_service_lst)/len(health_plan_customer_service_lst), 5)

health_Plan_Customer_Service_total_count = overAllpop_4("q34", "q35", "q36", "q37")

print(f"Health Plan Customer Service: {health_Plan_Customer_Service_total_count}")

# Getting needed Care
getting_care_tests_or_treatments_necessary = care_and_cordnate("q10", 4)
ease_of_getting_appointment_with_a_specialist = care_and_cordnate("q29", 4)

getting_needed_care_lst = [getting_care_tests_or_treatments_necessary["Score"], ease_of_getting_appointment_with_a_specialist["Score"]]
getting_needed_care = round(sum(getting_needed_care_lst)/len(getting_needed_care_lst), 5)

getting_needed_Care_total_count = overAllpop_2("q10", "q29")

print(f"Getting needed Care: {getting_needed_Care_total_count}")

# Getting Care Quickly
obtaining_needed_care_right_away = care_and_cordnate("q04", 4)
obtaining_care_when_needed = care_and_cordnate("q06", 4)
saw_person_came_to_see_within_15_mins = care_and_cordnate("q08", 4)

getting_care_quickly_lst = [obtaining_needed_care_right_away["Score"], obtaining_care_when_needed["Score"], saw_person_came_to_see_within_15_mins["Score"]]
getting_care_quickly = round(sum(getting_care_quickly_lst)/len(getting_care_quickly_lst), 5)

getting_Care_Quicklytotal_count = overAllpop_3("q04", "q06", "q08")

print(f"Getting Care Quickly: {getting_Care_Quicklytotal_count}")

# Getting Needed Prescription Drugs

ease_of_using_drug_plan_to_fill_rx_at_local_pharmacy = care_and_cordnate("q42", 4)
ease_of_using_drug_plan_to_fill_rx_by_mail = care_and_cordnate("q44", 4)
combined_local_pharmacy_and_mail = care_and_cordnate("q42_q44", 4)
ease_of_using_drug_plan_to_get_rx_medicines = care_and_cordnate("q40", 4)

getting_needed_prescription_drugs_lst = [ease_of_using_drug_plan_to_fill_rx_at_local_pharmacy["Score"], 
                                        ease_of_using_drug_plan_to_fill_rx_by_mail["Score"],
                                        combined_local_pharmacy_and_mail["Score"],
                                        ease_of_using_drug_plan_to_get_rx_medicines["Score"]]

getting_needed_rescription_drugs = sum(getting_needed_prescription_drugs_lst)/len(getting_needed_prescription_drugs_lst)

print(ease_of_using_drug_plan_to_fill_rx_at_local_pharmacy)
print(ease_of_using_drug_plan_to_fill_rx_by_mail)
print(combined_local_pharmacy_and_mail)
print(ease_of_using_drug_plan_to_get_rx_medicines)
print(getting_needed_rescription_drugs)
getting_Needed_Prescription_Drugs_total = overAllpop_5("q42", "q44", "q40", "q42", "q44")
print(f"Getting Needed Prescription Drugs: {getting_Needed_Prescription_Drugs_total}")

# Care Coordination
combined_item_test_results = care_and_cordnate("q20_q21", 4)
doctor_had_records_info_about_your_care = care_and_cordnate("q18", 4)
doctor_talked_about_prescription_medicines = care_and_cordnate("q23", 4)
got_help_managing_care_raw = care_and_cordnate("q26", 3) # Apply function before subtract 100 from below
got_help_managing_care = 100 - got_help_managing_care_raw["Score"]
doctor_informed_and_up_to_date = care_and_cordnate("q32", 4)

care_coordination_lst = [combined_item_test_results["Score"],
                        doctor_had_records_info_about_your_care["Score"],
                        doctor_talked_about_prescription_medicines["Score"],
                        got_help_managing_care,
                        doctor_informed_and_up_to_date["Score"]]
care_coordination = round(sum(care_coordination_lst)/ len(care_coordination_lst), 5)

care_Coordinationtotal_total_score = overAllpop_6( "q20", "q21", "q18", "q23", "q26", "q32")
print(f"Care Coordination: {care_Coordinationtotal_total_score}")



Result_dict = {"Rating the health Plan": {"Rating the health Plan": rating_of_Health_Plan},
               "Rating of Healthcare": {"Rating of Health care": rating_of_Health_Care},
               "Rating the drug plan": {"Rating the drug plan": rating_of_drug_plan},
               "Health Plan Customer Service": {"Getting information/help from customer service":getting_information_h,
                                                "Treated with courtesy and respect": treated_with_courtesy_respect,
                                                "Health plan forms easy to fill out": health_plan_forms_easy_to_fill_out,
                                                "Health Plan Customer Service Overall Score": health_plan_customer_service},
                "Getting needed Care": {"Getting care, tests, or treatments necessary": getting_care_tests_or_treatments_necessary,
                                        "Ease of getting appointment with a specialist": ease_of_getting_appointment_with_a_specialist,
                                        "Getting needed Care overall score": getting_needed_care},
               "Getting Care Quickly": {"Obtaining needed care right away": obtaining_needed_care_right_away,
                                        "Obtaining care when needed": obtaining_care_when_needed,
                                        "Saw person came to see within 15 mins": saw_person_came_to_see_within_15_mins,
                                        "Getting Care Quickly overall score": getting_care_quickly},
                "Getting Needed Prescription Drugs": {"Ease of using drug plan to fill rx at local pharmacy": ease_of_using_drug_plan_to_fill_rx_at_local_pharmacy,
                                                      "Ease of using drug plan to fill rx by mail": ease_of_using_drug_plan_to_fill_rx_by_mail,
                                                      "Combined Local Pharmacy and Mail": combined_local_pharmacy_and_mail,
                                                      "Ease of using drug plan to get rx medicines": ease_of_using_drug_plan_to_get_rx_medicines,
                                                      "Getting Needed Prescription Drugs overall score": getting_needed_rescription_drugs},
                "Care Coordination": {"Combined Item - Test Results": combined_item_test_results,
                                      "Doctor had records/info. about your care": doctor_had_records_info_about_your_care,
                                      "Doctor talked about prescription medicines": doctor_talked_about_prescription_medicines,
                                      "Got help managing care": [got_help_managing_care, got_help_managing_care_raw["Count"]],
                                      "Doctor informed and up-to-date": doctor_informed_and_up_to_date,
                                      "Care Coordination": care_coordination}}

doc = Document()

indent = "     "
for k, v in Result_dict.items():
    print(k)
    doc.add_heading(k, level=1)

    for key, value in v.items():
        print(f"{indent}{key} : {value}")
        p = doc.add_paragraph()
        p.add_run(f"{key}: {value}")
        p.paragraph_format.left = 30

doc.save("Output/Non_Disablity_Score.docx")






