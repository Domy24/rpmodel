ocm_base_url = "https://api.openchargemap.io/v3/poi/?"
graphhopper_route_base_url = "https://graphhopper.com/api/1/route?"
graphhopper_locations_base_url = "https://graphhopper.com/api/1/geocode?"
MAX_STATIONS = 10
MIN_DISTANCE = lambda length: length / 6
MAX_DISTANCE = lambda length: length / 3
MAX_RESULTS = 100
DISTANCE = 25
COUNTRY_ID_LIST = ("ALB, AND, ARM, AUT, AZE, BLR, BEL, BIH, BGR, CYP, HRV, DNK, EST, FIN, FRA, GEO, DEU, GRC, IRL, "
                   "ISL, ITA, KAZ, XKX, LVA, LIE, LTU, LUX, MKD, MLT, MDA, MCO, MNE, NLD, NOR, POL, PRT, CZE, ROU, "
                   "RUS, SMR, SRB, SVK, SVN, ESP, SWE, CHE, TUR, UKR, HUN, VAT")