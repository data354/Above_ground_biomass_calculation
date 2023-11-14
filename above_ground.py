import pandas as pd
import numpy as np


def lowers(x):
      return x.lower()

def str_trim(x):
  return x.strip()

def capitalize(x):
  return x.capitalize()

def  paste(x,y):
  return x+" "+y

def wd(x,y):
  if pd.isna(x) and pd.isna(y):
    return x
  elif pd.isna(y):
    return x
  else:
    return y

def replace(x):
  if isinstance(x, str):
    x =  x.replace(',','.')
    x = x.replace(' ','')
    return x
  else :
    return x

def transfert_wood_density(x,y):
  if pd.isna(x) and pd.isna(y):
    return x
  elif pd.isna(x):
    return y
  else:
    return x

## Allometic equation
def palm_biomass(Shade_tree_Height):
  return 10+ 6.4*float(Shade_tree_Height)

def citrus_biomass(Shade_tree_DBH):
  result =(-6.64 + 0.279*((Shade_tree_DBH*Shade_tree_DBH)*0.3142)+(0.000514*((Shade_tree_DBH*Shade_tree_DBH)*0.3142)**2))
  return result

def agb(WD,H,D):
  result =  0.0673*(WD*H*D**2)**0.976
  return result 

# Ramener les valeurs calculées à l'hectare
def hectare(x,superficie):
  val = ((x*10000)/(np.pi*superficie**2)) # ramner la valeur de biomass à l'unité (Kg/ha)
  #result = (val*10**6) # (Kg/ha)===> (Mg/ha)
  return val

##
def total_biomass(x,y):
  if not pd.isna(x) and not pd.isna(y):
    return x+y
  elif pd.isna(y):
    return x
  else:
    return y
  
##
def shade_tree_biomass(collect_file_path):
    
  carbon = pd.read_excel(collect_file_path,sheet_name = "GIZ FR Biomass plots_ Carbon...")
  Farm_identification =carbon[["IIdentifiant (ID) de la parcelle","_index"]]

  idd = Farm_identification[["IIdentifiant (ID) de la parcelle"]]
  idd.rename(columns={"IIdentifiant (ID) de la parcelle":"iidentifiant"},inplace=True)
  idd.drop_duplicates(inplace=True)

  ## next load the shade tree data
  shade = pd.read_excel(collect_file_path,sheet_name = "shade_trees_30m_plot")
  shade.drop_duplicates(inplace=True)

  # drop lines that we don't need
  tab = [i for i in range(10+1)]+[19,28,36,46,55,64,73,82,91,100,102]+[i for i in range(104,112)]
  reduced_dat = shade.drop(shade.iloc[:, tab],axis = 1)

  # define new file format
  shade_long_format = pd.DataFrame(columns=["_index","_parent_index","shade_tree1-Tree Nr.","shade_tree1-DBH (cm)",
                           "shade_tree1-Distance (m) (06 ou 6-30m)","shade_tree1-Bearing (°) (1.,2.,...8. Huitème)",
                           "shade_tree1-Height (m)","shade_tree1-Species or local name","Scientifique tree1-Species",
                           "shade_tree1-Notes"])
  
  # transpose columns to lines
  k = 0
  for shade in range(10):
      ##
      cols = [80,81]+[i for i in range(k,k+8)]
      X = reduced_dat.iloc[:,cols]
      mapping = {X.columns[0]: '_index', X.columns[1]: '_parent_index',X.columns[2]: 'shade_tree1-Tree Nr.',
                X.columns[3]: 'shade_tree1-DBH (cm)',X.columns[4]: 'shade_tree1-Distance (m) (06 ou 6-30m)',
                X.columns[5]: 'shade_tree1-Bearing (°) (1.,2.,...8. Huitème)',X.columns[6]: 'shade_tree1-Height (m)',
                X.columns[7]: 'shade_tree1-Species or local name', X.columns[8]: 'Scientifique tree1-Species',
                X.columns[9]: 'shade_tree1-Notes'}

      X = X.rename(columns=mapping)
      shade_long_format = pd.concat([shade_long_format,X])
      k = k+8

  # Next, you will need to add the "Farm_ID" into the new dataframe
  # rename "_index" column in Farm_identification data frame to "_parent_index" 
  # (this allows us to match everything by the _parent_index column)
  Farm_identification.rename(columns={"_index":"_parent_index"},inplace=True)

  # Use "_parent_index" to merge the Farm_ID
  combined_dat = shade_long_format.merge(Farm_identification, on="_parent_index")

  #rename columns
  combined_dat.rename(columns={"shade_tree1-Tree Nr.":"Shade_tree_number",
                              "shade_tree1-DBH (cm)":"Shade_tree_DBH",
                              "shade_tree1-Distance (m) (06 ou 6-30m)":"Shade_tree_Distance",
                              "shade_tree1-Bearing (°) (1.,2.,...8. Huitème)":"Shade_tree_Bearing",
                              "shade_tree1-Height (m)":"Shade_tree_Height",
                              "shade_tree1-Species or local name":"Species",
                              "Scientifique tree1-Species":"Scientific_name",
                              "shade_tree1-Notes":"Notes",
                              "IIdentifiant (ID) de la parcelle":"iidentifiant" },inplace=True)
  
  # drop columns that you don't need ("_index") and reorder columns for clarity
  cols = [10]+[i for i in range(2,10)]+[1]
  clean_dat = combined_dat.iloc[:,cols]

  # get rid of rows in that have NAs (only in columns 2,3,4,5,6) -
  # this is because Kobotoolbox generates columns for data even if it wasn't filled in i.e.
  # Farm number 121 might only have 5 shade trees recorded, yet the the kobotoolbox form has 10 spaces and registers tree 6- 10 as NAs
  shade_data_cleaned = clean_dat.dropna(subset =['Shade_tree_number', 'Shade_tree_DBH', 'Shade_tree_Distance','Shade_tree_Bearing','Shade_tree_Height'])

  # replace any missing species (that are NA in dataframe) with "Unknown"
  shade_data_cleaned['Scientific_name'] = shade_data_cleaned['Scientific_name'].fillna("Unknown")

  # now amend incorrect species names to correct names
  shade_data_cleaned["Scientific_name"]= shade_data_cleaned.apply(lambda x : lowers(x["Scientific_name"]),axis=1)
  shade_data_cleaned["Scientific_name"]= shade_data_cleaned.apply(lambda x : str_trim(x["Scientific_name"]),axis=1)

  # corriger le nom scientifique collecté
  shade_data_cleaned["Scientific_name"].replace({ "antiaris toxicaria subsp. africana":"antiaris toxicaria",
                                           "ceiba pentadra" : "ceiba pentandra",
                                           "citrus x sinensis" : "citrus sp",
                                            "celtis adolphi-fridericii" : "celtis adolfi-friderici",
                                            "arecaceae" : "elaeis guineensis",
                                            "guirbourtia ehie" : "guibourtia ehie",
                                            "nauclea diderichii" : "nauclea diderrichii",
                                            "polyathia oliveri" : "polyalthia suaveolens",
                                            "psidium goyava" : "psidium guajava",
                                            "raphia" : "elaeis guineensis",
                                            "samanea dinklagei" : "albizia spp",
                                            "spathodes campanulata" : "spathodea campanulata",
                                            "terminalia superpa" : "terminalia superba",
                                            "thieghemella heckelli" : "tieghemella heckelii",
                                            "myrianthus libericus rendle" : "myrianthus libericus",
                                            "scottelia klaineana var. mimfiensis" : "scottellia klaineana",
                                            "prunus domestica subsp. syriaca" : "prunus domestica",
                                            "afzelia bella var. gracilor" : "afzelia bella"},inplace=True)
  
  # Load GIZ wood density file
  wd_GIZ_data = pd.read_csv("data/wood_density_collect.csv")
  ## drop 1st column (not needed)
  wd_GIZ_data1 = wd_GIZ_data[["Scientific.name","Wood_density"]]

  ## change "Scientific.name" column to "Scientific_name" to match with "shade_data_cleaned1" dataset
  wd_GIZ_data1.rename(columns={"Scientific.name":"Scientific_name"},inplace=True)

  ## merge (by scientific name) with "shade_data_cleaned1" dataset
  shade_tree_cleaned_with_WD = shade_data_cleaned.merge(wd_GIZ_data1,on="Scientific_name",how="outer")

  ## reorder columns
  cols = [1,2,0,7,10,3,4,5,6,8,9] #c(2,3,1,8,11,4:7,9,10)
  shade_tree_cleaned_with_WD1 = shade_tree_cleaned_with_WD.iloc[:,cols]

  # Capitalize scientific name
  shade_tree_cleaned_with_WD1["Scientific_name"] = shade_tree_cleaned_with_WD1.apply(lambda x:capitalize(x["Scientific_name"]),axis=1)

  # Load DATA EXTRACT TO BIOMASS PACKAGE
  wddata = pd.read_csv("data/wdData.csv")

  ## group WD values for all species in BIOMASS database by genus and species and then get mean of WD
  wddata = wddata.groupby(['genus','species']).agg({'wd': 'mean'}).reset_index()
  wddata.rename(columns={"wd":'WD_mean'},inplace=True)

  ## Combine genus and species column and call it "Scientific.name" (to match with the species_list dataframe)
  wddata["Scientific_name"] = wddata.apply(lambda x: paste(x["genus"],x["species"]),axis=1)
  WD_data_for_merge = wddata[["WD_mean","Scientific_name"]]

  combined_data = shade_tree_cleaned_with_WD1.merge(WD_data_for_merge,on="Scientific_name",how="outer")
  data_with_species_and_WD_values = combined_data.dropna(subset =['iidentifiant'])

  # Now we need to transfer the WD values extracted from the biomass
  # package to cells with NAs in the "Wood_density" column
  data_with_species_and_WD_values["wds"] = data_with_species_and_WD_values.apply(lambda x:wd(x["Wood_density"],x["WD_mean"]),axis=1 )

  # Give the wood density of species that we have'nt in BIOMASS PACKAGE DATA
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Cola nitida","wds"]=0.6128958
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Cocos nucifera","wds"]=0.5
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Ficus variifolia","wds"]=0.4
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Dracaena arborea","wds"]=0.41825
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Morinda lucida","wds"]=0.5703
  data_with_species_and_WD_values.loc[data_with_species_and_WD_values["Scientific_name"]=="Sterculia tragacantha","wds"]=0.4457

  ## reorder the dataset and omit "WD_mean" column
  data_with_species_and_WD_values_clean = data_with_species_and_WD_values[["iidentifiant","Shade_tree_number","Species","Scientific_name",
                                                                          "Shade_tree_DBH","Shade_tree_Height","wds","Shade_tree_Distance",
                                                                           "Shade_tree_Bearing" ,"Notes" ,"_parent_index"]]

  # change column type
  data_with_species_and_WD_values_clean["Shade_tree_Height"] = data_with_species_and_WD_values_clean.apply(lambda x: replace(x["Shade_tree_Height"]),axis=1)
  data_with_species_and_WD_values_clean["Shade_tree_DBH"] = data_with_species_and_WD_values_clean.apply(lambda x: replace(x["Shade_tree_DBH"]),axis=1)
  data_with_species_and_WD_values_clean["Shade_tree_Height"] = pd.to_numeric(data_with_species_and_WD_values_clean["Shade_tree_Height"])
  data_with_species_and_WD_values_clean["Shade_tree_DBH"] = pd.to_numeric(data_with_species_and_WD_values_clean["Shade_tree_DBH"])
  
  ## CALCULATING BIOMASS
  ## Before you calculate biomass for all species.
  ## There are some species that will need species=specific equations (palms, citrus etc)

  # subset palm species: Elaeis guineensis and Cocos nucifera
  palms_only = data_with_species_and_WD_values_clean[(data_with_species_and_WD_values_clean["Scientific_name"]=="Elaeis guineensis")|(data_with_species_and_WD_values_clean["Scientific_name"]=="Cocos nucifera")]

  # create column called "biomass" and fill in using the AGB=10.0+6.4*H  equation from Brown 1997 paper:
  # Brown, S., 1997. Estimating Biomass and Biomass Change of Tropical Forests. A Primer. FAO, Forestry Paper no. 134.
  # (found in:"Asigbaase et al 2021, Biomass and carbon stocks of organic and conventional cocoa agroforest, Ghana" )
  palms_only["biomass_kg"] =  palms_only.apply(lambda x: palm_biomass(x["Shade_tree_Height"]),axis=1)

  # citrus: Citrus sinensis, Citrus sp
  citrus_only = data_with_species_and_WD_values_clean[(data_with_species_and_WD_values_clean["Scientific_name"]=="Citrus reticulata")|(data_with_species_and_WD_values_clean["Scientific_name"]=="Citrus sp")]

  ## any stem with a dbh less than 10cm has a negative biomass
  citrus_only["biomass_kg"] = citrus_only.apply(lambda x :citrus_biomass(x["Shade_tree_DBH"]),axis=1)

  ## Join the citrus and palm datasets together
  cit_and_palm = pd.concat([citrus_only,palms_only])

  # for woody species that don't have a wood density value (i.e unknown species that do not have WD values)
  #take the WD average of all trees in the same plot as the species with no WD and assign that mean value to
  #the unknown species
  WD_plot_mean = data_with_species_and_WD_values_clean.groupby(['iidentifiant']).agg({'wds': 'mean'}).reset_index()
  WD_plot_mean.rename(columns={"wds":'WD_mean'},inplace=True)

  ## merge two datasets by "iidentifiant"
  shade_species_all_data_clean = data_with_species_and_WD_values_clean.merge(WD_plot_mean, on="iidentifiant")

  ## move the values in the "WD_mean" column into the "Wood_density" column (only cells with NAs will be fillled with values )
  shade_species_all_data_clean["wds"] = shade_species_all_data_clean.apply(lambda x:transfert_wood_density(x["wds"],x["WD_mean"]),axis=1 )
  
  ## remove biomass_mean column
  shade_species_all_data_clean.drop(columns=["WD_mean"],inplace=True)

  ## calculate the biomass of the remaining woody species using biomass package
  ##library(BIOMASS)
  ## first subset out all the non-woody species
  woody_species_biomass = shade_species_all_data_clean[(shade_species_all_data_clean["Scientific_name"]!="Elaeis guineensis")&(shade_species_all_data_clean["Scientific_name"]!="Cocos nucifera")&(shade_species_all_data_clean["Scientific_name"]!="Citrus reticulata")&(shade_species_all_data_clean["Scientific_name"]!="Citrus sp")]
  woody_species_biomass.rename(columns={"wds":'Wood_density'},inplace=True)

  woody_species_biomass = woody_species_biomass[['iidentifiant','Species','Scientific_name','Shade_tree_DBH',
                                                 'Shade_tree_Height','Wood_density','Shade_tree_Distance']]

  
  woody_species_biomass["biomass_kg"] = woody_species_biomass.apply(lambda x : agb(x["Wood_density"],x["Shade_tree_Height"],x["Shade_tree_DBH"]),axis=1)

  # convert Mg to Kg
  #woody_species_biomass["biomass_kg"] = (woody_species_biomass["biomass_mg"]*10**-6)
  ## remove biomass_mean column
  #woody_species_biomass.drop(columns=["biomass_mg"],inplace=True)

  cit_and_palm.rename(columns={"wds":"Wood_density"},inplace=True)

  cit_and_palm = cit_and_palm[['iidentifiant', 'Species', 'Scientific_name', 
                               'Shade_tree_DBH','Shade_tree_Height', 'Wood_density', 
                               'Shade_tree_Distance','biomass_kg']]

  ##finally add the citrus and palm species data sets
  all_biomass_shade_data = pd.concat([woody_species_biomass,cit_and_palm])
  all_biomass_shade_data_total = all_biomass_shade_data.groupby(['iidentifiant']).agg({'biomass_kg': 'sum'}).reset_index()

  # Ramener les valeur à l'hectare:
  all_biomass_shade_data_total["biomass_mg_ha_shade"] = all_biomass_shade_data_total.apply(lambda x:hectare(x["biomass_kg"],30),axis=1)
  ## remove biomass_mean column
  all_biomass_shade_data_total.drop(columns=["biomass_kg"],inplace=True)

  # Coordonnées des zones d'études
  coordinate = carbon[["IIdentifiant (ID) de la parcelle","Latitude","Longitude"]]
  coordinate.rename(columns={"IIdentifiant (ID) de la parcelle":"iidentifiant"},inplace=True)
  coordinate["Longitude"] = coordinate.apply(lambda x : -x["Longitude"], axis=1)
  coordinate.drop_duplicates(inplace=True)

  # finale biomass
  biomass_shade_tree = coordinate.merge(all_biomass_shade_data_total,how="left")

  return biomass_shade_tree

###
def cocoa_tree_biomass(collect_file_path):
    
  carbon = pd.read_excel(collect_file_path,sheet_name = "GIZ FR Biomass plots_ Carbon...")
  Farm_identification =carbon[["IIdentifiant (ID) de la parcelle","_index"]]

  cocoa  =  pd.read_excel(collect_file_path,sheet_name = "cocoa_6m")

  tab = list(range(0,7))+[10,14,18,22,26,30,34,38,42,46,50,54,56]+ list(range(58,66))
  reduced_cacao_dat  =  cocoa.drop(cocoa.iloc[:, tab],axis = 1)

  # define new csv file format
  cacao_long_format = pd.DataFrame(columns=["_index","_parent_index","cocoa_1-Cocoa tree No.",
                                            "cocoa_1-D30 (cm)","cocoa_1-Notes"])
  
  # transpose columns to  lines
  k = 0
  for shade in range(12):
      ##
      cols = [36,37]+[i for i in range(k,k+3)]
      X = reduced_cacao_dat.iloc[:,cols]
      mapping = {X.columns[0]: '_index', X.columns[1]: '_parent_index',X.columns[2]: 'cocoa_1-Cocoa tree No.',
                X.columns[3]: 'cocoa_1-D30 (cm)',X.columns[4]: 'cocoa_1-Notes'}

      X = X.rename(columns=mapping)
      cacao_long_format = pd.concat([cacao_long_format,X])
      k = k+3

  # Next, you will need to add the "Farm_ID" into the new dataframe
  # rename "_index" column in Farm_identification data frame to "_parent_index" 
  # (this allows us to match everything by the _parent_index column)
  Farm_identification.rename(columns={"_index":"_parent_index"},inplace=True)
  
  ## add the "Farm_ID" into the new dataframe
  ### then use the "_parent_index" to merge the Farm_ID
  combined_dat_cacao = cacao_long_format.merge(Farm_identification, on="_parent_index")

  # reneme columns
  combined_dat_cacao.rename(columns={"IIdentifiant (ID) de la parcelle":"iidentifiant",
                                   "cocoa_1-Cocoa tree No.":"Cacao_tree_number",
                                   "cocoa_1-D30 (cm)":"Cacao_tree_diam30",
                                   "cocoa_1-Notes":"Cacao_tree_notes"},inplace=True)
  
  ## In the "Cacao_tree_diam30" to replace any commas (,) with a decimal point (.)
  combined_dat_cacao["Cacao_tree_diam30"] = combined_dat_cacao.apply(lambda x: replace(x["Cacao_tree_diam30"]),axis=1)
  ## make Shade_tree_DBH and Shade_tree_Height columns numeric
  combined_dat_cacao["Cacao_tree_diam30"] = pd.to_numeric(combined_dat_cacao["Cacao_tree_diam30"])

  ## get rids of rows in that have NAs (only if they appear in columns 2 and 3, as these will be non-entries)
  cacao_data_cleaned = combined_dat_cacao.dropna(subset =["Cacao_tree_number","Cacao_tree_diam30"])

  ##. CALCULATE BIOMASS FOR COCOA TREES 

  ## add column for biomass calculation then calculate using the allometric equation found in "Asigbaase et al 2021, Biomass and carbon stocks of organic and conventional cocoa agroforest, Ghana").
  ## equation:  10(− 1.625 + 2.63 * log(DBH))  so this would be 10(− 1.625 + 2.63 * log(D_30))
  cacao_data_cleaned["biomass_kg"]  =  cacao_data_cleaned.apply(lambda x : 10*(-1.625 + 2.63 * np.log(x["Cacao_tree_diam30"])),axis=1)

  cacao_data_cleaned_total = cacao_data_cleaned.groupby(['iidentifiant']).agg({'biomass_kg': 'sum'}).reset_index()

  cacao_data_cleaned_total["biomass_mg_ha_cocoa"] = cacao_data_cleaned_total.apply(lambda x:hectare(x["biomass_kg"],6),axis=1)

  ## remove biomass_mean column
  cacao_data_cleaned_total.drop(columns=["biomass_kg"],inplace=True)

  return cacao_data_cleaned_total

##
def biomass_finale(shade_trees_biomass,cocoa_trees_biomass,save_name):
    above_ground_biomass = shade_trees_biomass.merge(cocoa_trees_biomass,how="left")
    above_ground_biomass["biomass_mg_ha"] = above_ground_biomass.apply(lambda x : total_biomass(x["biomass_mg_ha_shade"],x["biomass_mg_ha_cocoa"]),axis=1)
    path = "data/"+save_name+".csv"
    #above_ground_biomass.to_csv(path,index=False)

    return above_ground_biomass