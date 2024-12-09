import re
import pandas as pd

def categorize_topics(topic,value_set):
    none = 1
    # Medicine and Health Sciences
    if re.search(r"(Medicine|Health|Clinical|Medical|Nursing|Pharmaceutical|Pharmacology|Toxicology|Dentistry|Veterinary|Surgery|Pathology|Psychiatry|Anatomy|Physiology|Immunology|Microbiology|Oncology|Radiology|Neurology|Cardiology|Gastroenterology|Hepatology|Nephrology|Urology|Dermatology|Ophthalmology|Otorhinolaryngology|Obstetrics|Gynecology|Pediatrics|Geriatrics|Gerontology|Rehabilitation|Orthopedics|Anesthesiology|Emergency Medicine|Public Health|Epidemiology|Nutrition|Dietetics)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Medicine and Health Sciences")
    # Engineering and Technology
    if re.search(r"(Engineering|Technology|Aerospace|Automotive|Biomedical|Chemical|Civil|Electrical|Electronic|Industrial|Manufacturing|Mechanical|Nuclear|Ocean|Geotechnical|Materials Science|Polymers|Plastics|Ceramics|Composites|Metals|Alloys|Building|Construction|Architecture|Instrumentation|Energy|Power|Renewable|Sustainable|Pollution|Waste Management|Environmental Engineering|Fuel Technology|Catalysis|Process Chemistry|Filtration|Separation|Fluid Flow|Transfer Processes|Surfaces|Interfaces|Coatings|Films|Electrochemistry|Corrosion)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Engineering and Technology")        
    # Computer Science and Information Technology
    if re.search(r"(Computer Science|Software|Hardware|Architecture|Artificial Intelligence|Machine Learning|Data Mining|Information Systems|Management|Networks|Communications|Internet|Cybersecurity|Human-Computer Interaction|Computer Vision|Pattern Recognition|Signal Processing|Modeling|Simulation|Computational|Theoretical Computer Science|Media Technology|Computer Graphics|Computer-Aided Design)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Computer Science and Information Technology")        
    # Chemistry and Materials Science
    if re.search(r"(Chemistry|Biochemistry|Molecular Biology|Chemical Engineering|Materials Science|Organic Chemistry|Inorganic Chemistry|Physical Chemistry|Analytical Chemistry|Theoretical Chemistry|Polymer|Materials Chemistry|Spectroscopy|Electrochemistry|Colloid|Surface Chemistry|Catalysis|Biomaterials|Nanotechnology)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Chemistry and Materials Science")
    # Physics and Astronomy
    if re.search(r"(Physics|Astronomy|Astrophysics|Nuclear|Particle|Atomic|Molecular|Optics|Condensed Matter|Quantum|Statistical|Nonlinear|Mathematical Physics|Acoustics|Ultrasonics|Radiation|Space|Planetary Science)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Physics and Astronomy")
    # Environmental Science and Sustainability
    if re.search(r"(Environmental Science|Ecology|Sustainability|Renewable Energy|Pollution|Waste Management|Environmental Engineering|Climate Change|Global Warming|Conservation|Biodiversity|Ecosystems|Natural Resources|Water Science|Oceanography|Atmospheric Science|Soil Science|Geology|Geophysics|Geochemistry|Paleontology|Earth Science|Environmental Chemistry)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Environmental Science and Sustainability")
    # Biology and Life Sciences
    if re.search(r"(Biology|Biochemistry|Molecular Biology|Genetics|Cell Biology|Microbiology|Immunology|Biotechnology|Bioengineering|Biophysics|Neuroscience|Zoology|Botany|Plant Science|Animal Science|Ecology|Evolution|Systematics|Developmental Biology|Structural Biology|Physiology|Anatomy|Pathology|Parasitology|Virology|Mycology|Marine Biology|Aquatic Science|Forestry|Agriculture|Agronomy|Horticulture|Food Science)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Biology and Life Sciences")        
    # Social Sciences and Humanities
    if re.search(r"(Social Sciences|Humanities|Psychology|Sociology|Political Science|Anthropology|Linguistics|Language|Literature|History|Philosophy|Arts|Music|Visual Arts|Performing Arts|Religious Studies|Cultural Studies|Gender Studies|Education|Law|Library Science|Information Science|Communication|Media Studies|Journalism|Geography|Urban Studies|Demography|Archeology)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Social Sciences and Humanities")            
    # Business, Management and Economics
    if re.search(r"(Business|Management|Accounting|Finance|Economics|Econometrics|Marketing|Strategy|Operations Research|Human Resources|Organizational Behavior|Leadership|Entrepreneurship|International Business|Tourism|Hospitality|Management Information Systems)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Business, Management and Economics")
    # Mathematics and Statistics
    if re.search(r"(Mathematics|Statistics|Probability|Algebra|Number Theory|Geometry|Topology|Calculus|Analysis|Numerical Analysis|Discrete Mathematics|Combinatorics|Logic|Mathematical Modeling|Computational Mathematics|Applied Mathematics)", topic, re.IGNORECASE):
        none = 0
        value_set.add("Mathematics and Statistics")
    
    if(none):
        value_set.add("Other")

import pandas as pd

def process_csv(filepath, source_col, existing_col):
    """
    Processes a CSV file to replace an existing column with sorted sets of values.

    Args:
        filepath: Path to the CSV file.
        source_col: Name of the column containing strings to be split.
        existing_col: Name of the existing column to be replaced.
    """

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    # No need to initialize the existing column

    for index, row in df.iterrows():
        cell_value = row[source_col]
        if pd.isna(cell_value):
            df.at[index, existing_col] = set()
            continue

        split_items = cell_value.split(';')
        value_set = set()
        for item in split_items:
            item = item.strip()
            if item:
                categorize_topics(item,value_set)
        data = sorted(list(value_set))
        df.at[index, existing_col] = "; ".join(data)
    df.to_csv(filepath, index=False)
    print(f"Processed CSV. Column '{existing_col}' updated.")


filepath = "C:/Users/Public/Documents/My/DataSci/DSDE_Final_Project_WARK/Data_Aj/2/joined_2018-2023.csv"  # Replace with your CSV file path
source_col = "subject_area_name" 
existing_col = "category"  

process_csv(filepath, source_col, existing_col)
