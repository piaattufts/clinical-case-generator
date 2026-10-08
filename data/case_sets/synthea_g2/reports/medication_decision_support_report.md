# Medication decision support

## G2-001
- cephalexin: stop (CEPHALEXIN_UTI_500_BID); evidence mh-treat, mh-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence mh-base, mh-meds
- aspirin: continue (ASPIRIN_81_DAILY); evidence mh-base, mh-meds
- metoprolol: continue (METOPROLOL_TARTRATE_BID); evidence mh-base, mh-meds
- ibuprofen: continue (IBUPROFEN_400_PRN); evidence mh-base, mh-meds
- lisinopril: continue (LISINOPRIL_10_DAILY); evidence mh-base, mh-meds

## G2-002
- lisinopril: stop (LISINOPRIL_10_DAILY); evidence mh-meds, mh-response
- hydrochlorothiazide: continue (HCTZ_25_DAILY); evidence mh-base, mh-meds
- ibuprofen: continue (IBUPROFEN_400_PRN); evidence mh-base, mh-meds
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence mh-base, mh-meds

## G2-003
- hydrochlorothiazide: stop (HCTZ_25_DAILY); evidence mh-meds, mh-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence mh-base, mh-meds
- tacrolimus: continue (TACROLIMUS_ER_1MG_DAILY); evidence mh-base, mh-meds
- lisinopril: continue (LISINOPRIL_10_DAILY); evidence mh-base, mh-meds
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence mh-base, mh-meds

## G2-004
- azithromycin: stop (AZITHROMYCIN_CAP_CONTINUATION); evidence mh-treat, mh-response
- aspirin: continue (ASPIRIN_81_DAILY); evidence mh-base, mh-meds
- atorvastatin: continue (ATORVASTATIN_20_DAILY); evidence mh-base, mh-meds
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence mh-base, mh-meds
- ibuprofen: continue (IBUPROFEN_400_PRN); evidence mh-base, mh-meds

## G2-005
- furosemide: new_start (FUROSEMIDE_40_DAILY); evidence hf-treat, hf-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hf-baseline, hf-response, hf-ready
- lisinopril: continue (LISINOPRIL_10_DAILY); evidence hf-baseline, hf-response, hf-ready
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence hf-baseline, hf-response, hf-ready

## G2-006
- lisinopril: restart (LISINOPRIL_10_DAILY); evidence hf-baseline, hf-treat, hf-response
- furosemide: new_start (FUROSEMIDE_40_DAILY); evidence hf-treat, hf-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hf-baseline, hf-response, hf-ready
- warfarin: continue (WARFARIN_INR_INDIVIDUALIZED); evidence hf-baseline, hf-response, hf-ready

## G2-007
- furosemide: new_start (FUROSEMIDE_40_DAILY); evidence hf-treat, hf-response
- metoprolol: new_start (METOPROLOL_SUCCINATE_DAILY); evidence hf-precip, hf-response
- hydrochlorothiazide: continue (HCTZ_25_DAILY); evidence hf-baseline, hf-response, hf-ready
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence hf-baseline, hf-response, hf-ready

## G2-008
- furosemide: new_start (FUROSEMIDE_40_DAILY); evidence hf-treat, hf-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hf-baseline, hf-response, hf-ready
- warfarin: continue (WARFARIN_INR_INDIVIDUALIZED); evidence hf-baseline, hf-response, hf-ready
- lisinopril: continue (LISINOPRIL_10_DAILY); evidence hf-baseline, hf-response, hf-ready

## G2-009
- ceftriaxone: continue (CEFTRIAXONE_ENDOCARDITIS_OPAT); evidence en-work, en-treat, en-response, en-ready

## G2-010
- ceftriaxone: continue (CEFTRIAXONE_ENDOCARDITIS_OPAT); evidence en-work, en-treat, en-response, en-ready

## G2-011
- ceftriaxone: continue (CEFTRIAXONE_ENDOCARDITIS_OPAT); evidence en-work, en-treat, en-response, en-ready

## G2-012
- ceftriaxone: continue (CEFTRIAXONE_ENDOCARDITIS_OPAT); evidence en-work, en-treat, en-response, en-ready

## G2-013
- tacrolimus: continue (TACROLIMUS_ER_1MG_DAILY); evidence tx-base, tx-treat, tx-response
- valganciclovir: new_start (VALGANCICLOVIR_CMV_TREATMENT); evidence tx-work, tx-dx, tx-treat, tx-response
- hydrochlorothiazide: continue (HCTZ_25_DAILY); evidence tx-base, tx-ready
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence tx-base, tx-ready

## G2-014
- tacrolimus: continue (TACROLIMUS_ER_1MG_DAILY); evidence tx-base, tx-treat, tx-response
- valganciclovir: new_start (VALGANCICLOVIR_CMV_TREATMENT); evidence tx-work, tx-dx, tx-treat, tx-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence tx-base, tx-ready
- lisinopril: continue (LISINOPRIL_10_DAILY); evidence tx-base, tx-ready

## G2-015
- tacrolimus: continue (TACROLIMUS_ER_1MG_DAILY); evidence tx-base, tx-treat, tx-response
- valganciclovir: dose_change (VALGANCICLOVIR_CMV_TREATMENT); evidence tx-work, tx-dx, tx-treat, tx-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence tx-base, tx-ready
- hydrochlorothiazide: continue (HCTZ_25_DAILY); evidence tx-base, tx-ready
- amlodipine: continue (AMLODIPINE_2_5_DAILY); evidence tx-base, tx-ready

## G2-016
- tacrolimus: continue (TACROLIMUS_ER_1MG_DAILY); evidence tx-base, tx-treat, tx-response
- valganciclovir: new_start (VALGANCICLOVIR_CMV_TREATMENT); evidence tx-work, tx-dx, tx-treat, tx-response
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence tx-base, tx-ready

## G2-017
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence hip-base, hip-treat, hip-response, hip-ready
- enoxaparin: stop (ENOXAPARIN_HOSPITAL_PROPHYLAXIS); evidence hip-treat, hip-ready
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hip-base, hip-ready

## G2-018
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence hip-base, hip-treat, hip-response, hip-ready
- enoxaparin: stop (ENOXAPARIN_HOSPITAL_PROPHYLAXIS); evidence hip-treat, hip-ready
- aspirin: continue (ASPIRIN_81_DAILY); evidence hip-base, hip-ready

## G2-019
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence hip-base, hip-treat, hip-response, hip-ready
- enoxaparin: stop (ENOXAPARIN_HOSPITAL_PROPHYLAXIS); evidence hip-treat, hip-ready
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hip-base, hip-ready

## G2-020
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence hip-base, hip-treat, hip-response, hip-ready
- enoxaparin: stop (ENOXAPARIN_HOSPITAL_PROPHYLAXIS); evidence hip-treat, hip-ready
- aspirin: continue (ASPIRIN_81_DAILY); evidence hip-base, hip-ready
- metoprolol: continue (METOPROLOL_SUCCINATE_100_DAILY); evidence hip-base, hip-ready

## G2-021
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence gi-base, gi-work, gi-response, gi-ready
- pantoprazole: new_start (PANTOPRAZOLE_40_DAILY); evidence gi-work, gi-response

## G2-022
- warfarin: restart (WARFARIN_INR_INDIVIDUALIZED); evidence gi-base, gi-work, gi-response, gi-ready
- pantoprazole: new_start (PANTOPRAZOLE_40_DAILY); evidence gi-work, gi-response

## G2-023
- warfarin: hold (WARFARIN_INR_INDIVIDUALIZED); evidence gi-base, gi-work, gi-response, gi-ready

## G2-024
- warfarin: hold (WARFARIN_INR_INDIVIDUALIZED); evidence gi-base, gi-work, gi-response, gi-ready
