
# sample usage:  daily_dev = 100 / math.exp(DEVELOPMENT_ALPHA * math.exp(DEVELOPMENT_BETA * degree_day))
DEVELOPMENT_ALPHA = 6.002994
DEVELOPMENT_BETA = -0.03070758

sex_dict = {"M": "Male",
            "Male": "Male",
            "Female": "Female",
            "Immature": "Immature",
            "F": "Female",
            "IT": "Immature",
            "I": "Immature"}

# Pairing priority options
prio_dict = {"H": "High",
             "M": "Medium",
             "L": "Low",
             "P": "Pairwise",
             "E": "Extra Male"}

sfa_nums = [15, 16, 17, 18, 19, 20, 21, 22, 23]

collection_evntc_list = ["electrofishing", "bypass collection", "smolt wheel collection", "smolt collection",
                         "fall parr collection"]

collection_locc_list = ["Adult Collection Site", "Bypass Site", "Electrofishing Site", "Smolt Wheel Site"]
distribution_locc_list = ["Distribution Site"]

egg_dev_evntc_list = ["egg development", "heath unit transfer", "picking", "shocking"]

in_out_dict = {None: "", False: "Origin", True: "Destination"}

absolute_codes = ["Egg Count", "Fish Count", "Counter Count", "Fecundity Estimate"]
add_codes = ["Fish in Container", "Photo Count", "Eggs Added", "Fish Caught"]
subtract_codes = ["Mortality", "Pit Tagged", "Egg Picks", "Shock Loss", "Cleaning Loss", "Spawning Loss",
                  "Eggs Removed",
                  "Fish Removed from Container", "Fish Distributed"]