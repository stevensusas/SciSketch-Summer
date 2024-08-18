import pandas as pd

journals = [
    "Cell",
    "Cancer Cell",
    "Cell Chemical Biology",
    "Cell Genomics",
    "Cell Host & Microbe",
    "Cell Metabolism",
    "Cell Reports",
    "Cell Reports Medicine",
    "Cell Stem Cell",
    "Cell Systems",
    "Current Biology",
    "Developmental Cell",
    "Immunity",
    "Med",
    "Molecular Cell",
    "Neuron",
    "Structure",
    "American Journal of Human Genetics",
    "Biophysical Journal",
    "Biophysical Reports",
    "Human Genetics and Genomics Advances",
    "Molecular Plant",
    "Molecular Therapy",
    "Molecular Therapy Methods & Clinical Development",
    "Molecular Therapy Nucleic Acids",
    "Molecular Therapy Oncology",
    "Plant Communications",
    "Stem Cell Reports",
    "Trends in Biochemical Sciences",
    "Trends in Cancer",
    "Trends in Cell Biology",
    "Trends in Ecology & Evolution",
    "Trends in Endocrinology & Metabolism",
    "Trends in Genetics",
    "Trends in Immunology",
    "Trends in Microbiology",
    "Trends in Molecular Medicine",
    "Trends in Neurosciences",
    "Trends in Parasitology",
    "Trends in Pharmacological Sciences",
    "Trends in Plant Science",
    "Cell Reports Physical Science",
    "Chem",
    "Chem Catalysis",
    "Device",
    "Joule",
    "Matter",
    "Newton",
    "Trends in Chemistry",
    "Cell Reports Methods",
    "Cell Reports Sustainability",
    "Heliyon",
    "iScience",
    "One Earth",
    "Patterns",
    "STAR Protocols",
    "Nexus",
    "The Innovation",
    "Trends in Biotechnology",
    "Trends in Cognitive Sciences"
]

# Load the CSV file
input_file = 'science_direct_results.csv'
output_file = 'cell_journal_results.csv'

# Read the CSV file
df = pd.read_csv(input_file)

# Filter the DataFrame to keep only rows where sourceTitle is exactly "Cell"
cell_df = df[df['sourceTitle'] == 'Cell']

# Display some information about the filtered DataFrame
print(f"Total rows in original DataFrame: {len(df)}")
print(f"Rows with sourceTitle 'Cell': {len(cell_df)}")

# Display the first few rows of the filtered DataFrame
print("\nFirst few rows of the filtered DataFrame:")
print(cell_df.head())

# Save the filtered DataFrame to a new CSV file
cell_df.to_csv(output_file, index=False)
print(f"\nFiltered results saved to {output_file}")