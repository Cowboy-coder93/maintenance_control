criticals = {
        ############
        ##Combat Support Systems
        ############
        "10K FORKLIFT": {
                         "TRK LFT FK VAR RCH RT": "014172886",
                         "TRK LIFT FORK": "015536676"
                        },
        "5K FORKLIFT": {
                        "LIGHT CAPABILITY FORK LIFT": "015999978"
                       },
        "4K FORKLIFT": {
                        "TRK LF FK 4K W/O CAB": "0133008907"
                       },
        "M984 WRECKER": {
                        "M984A4WO/W": "015342245",
                        "M984A2R1": "014928233"
                       },
        "M978 FUELER": {
                        "M978A2R1WW": "14928226",
                        "M978A4WOW": "15341117",
                        "M978A2WW": "14928216"
                       },
        "M1089 WRECKER": {
                          "M1089A1WW": "014473892"
                         },
        "WATER BUFFALO": {
                          "TANK, WATER, TRLR MTD": "010915167", #Needs more entries
                          "M1112": "013899073",
                          "M149A2": "011087367"
                         },
        "SRPT": {
                 "M1032": "011307980"
                },
        "M977 LRPT": {
                       "M977A4WOW": "015341091"
                     },
        "BMC/BME": {
                     "BME": "011348713",
                    "BMC": "014493438"
                    },
        "AN/T CM-1": {
                      "TCM1": "011820578"
                     },
        ############
        ##C4I
        ############
        "MIDS": {
                 "RADIO SET": "015477436",
                 "RAS AN/USQ-140(V)2(C)": "014954062"
                },
        "JTT": {
                "RECEIVER, RADIO": "015844467"
               },
        "BCP": {
                "BATT COM POS": "015308714"
               },
        "TCS": {
                "M934A2": "014258319"
               },
        "PSC-5 SATC": {
                       "PSC5D": "014830568",
                       "PSC5": "013664120",
                      },
        "VSAT": {
                 "AN/TSC-183": "015591209"
                },
        ############
        ##Commo
        ############
        "RT1523": {
                   "RT1523EC": "014441219",
                   "RT-1523F(C)/": "015353667" 
                  },
        "RT1694D": {
                    "RECEIVER-TRANSMIT,RADIO:RT-1694D(P)(C)/U": "014963523"
                   },
        "RT1720G": {},
        "VRC-104": {
                    "VRC-104": "015759305"
                   }, #only category, g2g
        "VRC89F": {
                   "VRC89F": "014518247"
                  }, #only cat g2g
        "VRC90A": {
                   "VRC90A": "0000000"
                  }, #only cat g2g WE DO NOT HAVE THESE OH
        "VRC90F": {
                   "VRC90F": "014518246"
                  }, #Wrong, we have 40 instead of a ton
        "VRC91F": {
                   "VRC91F": "014518249"
                  }, #only cat g2g
        "VRC92A": {
                   "VRC92A": "014518246"
                  }, #only cat g2g
        "VRC92F": {
                   "VRC92F": "014518250"
                  }, #only cat g2g
        "SKL": {
                "AN/PYQ-10(C(": "015173587", 
                "AN/PYZ-10A": "016444375" 
               },
        "KG175D": {
                   "KG 175D": "015474520"
                  }, #only cat g2g
        "KIV 7": {
                  "KIV 7 M": "015302811"
                 }, #g2g
        ############
        ##Power Generation
        ############
        "DRASH": {
                  "DRASHA": "014991814",
                  "DRASHB": "014594366"
                 },
        "3KW": {
                "MEP831": "012853012"
               }, #correct (4)
        "5KW": {
                "MEP802A": "012747387"
               }, #correct (5)
        "10KW": {
                 "MEP803A": "012755061", 
                 "PU798A": "014133818",
                 "PU406BM": "003949576", 
                 "MEP813A": "012747392"
                },#NOT CORRECT (7 v 13)
        ############
        ##Weapons Systems
        ############
        "M16A2": {
                  "M16A2RIFLE": "011289936"
                 },
        "M9": {
                "M9": "011182640"
              },
        "M249":  { "M249MG": "011277510",
                   "M249": "014516769"
                 },
        "M2A1": {
                "M2A1": "015111250"
                },
        "MK19": {
                "MK19": "014909697"
                }, 
        "M240B": {
                  "M240B": "014123129"
                 }, #g2g
        ############
        ##Gas Mask
        ############
        "GAS MASK": {
                     "M50": "015124434",
                     "M-50": "015124431",
                     "MASK SYSTEM CHEMICA": "015124435",
                     "MASK SYSTEM CHEMIC": "015124436",
                     "MASK SYSTEM CHEMICL": "015124437",
                     "MASK SYSTEM CHEMICAL": "015124429"
                     }, #Not everyone uploaded their mask
        "CHEM DET": {
                    #"AN/PSS-14",
                     #"M4"]
                     }, #Do not know Model number
        "MINE DET": {
                    #"PSS12"]
                    }, #Other mine detectors lack model number
        "NVG": {
                "PVS14": "014320524", 
                "NIGHT VISION DEVICE, AN/PVS14-3: AMERICA": "01C023219",
                "AN/PVS-7B": "012280937",
                "AN/PVS 7D": "014225413"
                },
        ############
        ##HMMWV Family
        ############
        "FLA": {
                #["M997A3"
                },
        "ISE CONTACT": {}
}

wb_name = "ESR.XLSX"

import openpyxl

wb = openpyxl.load_workbook(wb_name)
wb_activ = wb.active
niin = 'H'
bumper = 'C'
i = 2

aggregate_dict = {}
bumper_tracker = []
while True:
    cell = niin+str(i)
    bumper_cell = bumper+str(i)
    if len(wb_activ[cell].value) != 0:
        #Perform the check by looping thru 
        for area in criticals:
            for specific_area in criticals[area]:
                if len(criticals[area]) == 0:
                    continue
                else:
                    for k,v in criticals[area].items():
                        if v == wb_activ[cell].value:
                            if wb_activ[bumper_cell].value not in bumper_tracker:
                                bumper_tracker.append(wb_activ[bumper_cell].value)
                                if area in aggregate_dict:
                                    aggregate_dict[area] = aggregate_dict[area]+1
                                else:
                                    aggregate_dict[area] = 1
                                
        i += 1
    else:
        break

    
"""
Search for E11-15
Check for FLA model number ctrl+f
"""

"""
Grab the Niin of each dictionary

"""