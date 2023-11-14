# ABOVE GROUND BIOMASS CALCULATION


**ABOVE GROUND BIOMASS CALCULATION**, is an application for calculating above ground biomass density (AGBD), based on field measurements (height, diameter, scientific name of trees), carried out by foresters. The application takes as input a file which contains these different measurements and calculates the AGBD based on allometric equations depending on the species.

We use 4 equations depending on the species for the AGBD calculation. Described below

## EQUATIONS

### Eq1 : palm species
 **10 + 6.4*tree_Height**

 (https://www.fao.org/3/W4095E/w4095e06.htm#3.%20methods%20for%20estimating%20biomass%20density%20from%20existing%20data)

### Eq2 : citrus species
 **-6.64 + 0.279*(tree_DBH*tree_DBH*0.3142)+(0.000514* (tree_DBH*tree_DBH*0.3142)^2)**

(https://www.scirp.org/(S(lz5mqp453edsnp55rrgjct55.))/journal/paperinformation.aspx?paperid=86643)

### Eq3 : cocoa species
 **10*(-1.625 + 2.63*log(Cacao_tree_diam))**

(allometric equation found in "Asigbaase et al 2021, Biomass and carbon stocks of organic and conventional cocoa agroforest, Ghana")

### Eq4 : others species
 **0.0673*(Wood_density*Height*(Diameter)^2)^0.976**

(https://cran.r-project.org/web/packages/BIOMASS/BIOMASS.pdf)


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
