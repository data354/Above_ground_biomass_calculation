# ABOVE GROUND BIOMASS CALCULATION


**ABOVE GROUND BIOMASS CALCULATION**, is an application for calculating above ground biomass density (AGBD), based on field measurements (height, diameter, scientific name of trees), carried out by foresters. The application takes as input a file which contains these different measurements and calculates the AGBD based on allometric equations depending on the species.

## OPERATIONS
Once we pass the field measurements file as input to the application, the AGBD calculation process starts. First, suppose that there are different plots (collection zones) during the study, we take the species individually (scientific name) which we match with a csv file extracted from the BIOMASS library of R, which contains the wood density of more than 16,000 species. This allows us to find the density of the species in question if it is found in the csv file, this process is repeated for all species in each study area. Once this is complete, we separate our species into 4 categories (palm, citrus, cocoa, and other). For the first three categories mentioned, the calculation of their biomass does not require a priori knowledge of the wood density, on the other hand for the species found in the 'other' category it is necessary to know their wood density, so we filter these by removing the species whose density we were unable to obtain. It should be noted that species whose density is unknown are not taken into account during our biomass calculation and they are notified to users in the logs. Next, we move on to calculating the biomass itself, calling the corresponding allometric equation (see the equation section) for each category. Finally, after calculation we obtain the biomass in kg for each species, an aggregation step follows by summing all the biomass values ​​for each study area which gives us a biomass value in Kg/area_of_the_plot . In our case, the study areas being circles of radius 30 m, we obtain biomass values ​​for each study area in Kg/2826 m^2 values ​​which we ultimately reduce to Kg/ha, and this is this last value that is returned to users for each plot.



We use 4 equations depending on the species for the AGBD calculation. Described below

## EQUATIONS

### Eq1 : palm species [(source)](https://www.fao.org/3/W4095E/w4095e06.htm#3.%20methods%20for%20estimating%20biomass%20density%20from%20existing%20data)

 **10 + 6.4\*tree_Height** 

 
### Eq2 : citrus species [(source)](https://www.scirp.org/(S(lz5mqp453edsnp55rrgjct55.))/journal/paperinformation.aspx?paperid=86643)

 **-6.64 + 0.279\*(tree_DBH\*tree_DBH\*0.3142)+(0.000514\* (tree_DBH\*tree_DBH\*0.3142)^2)**


### Eq3 : cocoa species (allometric equation found in "Asigbaase et al 2021, Biomass and carbon stocks of organic and conventional cocoa agroforest, Ghana")

 **10\*(-1.625 + 2.63\*log(Cacao_tree_diam))**


### Eq4 : others species [(source)]((https://cran.r-project.org/web/packages/BIOMASS/BIOMASS.pdf))

 **0.0673\*(Wood_density\*Height\*(Diameter)^2)^0.976**


## Prerequisites

- [x] Make sure all the library in requirements are install.

## Installation

To install the ABOVE GROUND BIOMASS CALCULATION app, follow these steps:

1. Clone the repository to your local machine, then open the project folder.

2. Start the application

You can  use the following command to start the app:
`streamlit run app.py`

3. Use the application

Once the server is up and running, you can access by going to `http://localhost:8501/` or `http://192.168.86.36:8501/` in your web browser.

This is the running applications interface 
<img width="1440" alt="Screenshot 2023-11-14 at 16 14 12" src="https://github.com/data354/Above_ground_biomass_calculation/assets/103064728/761c57b4-4b10-4351-8eb9-5dc8de0feedf">


That's it! You should now be able to use AGBD application. If you have any questions or problems, please don't hesitate to contact us at "issouf.toure@data354.co"
