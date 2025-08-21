import pandas as pd
import os

# Load dataset
file_path = "data/skills_data.csv"  # Ensure the correct path
output_dir = "data/processed_data"
output_path = os.path.join(output_dir, "processed_skills_data.csv")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the dataset
try:
    df = pd.read_csv(file_path)
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print(f"❌ Error: File '{file_path}' not found. Please check the path.")
    exit()

# Display initial dataset info
print("\n🔹 Initial Dataset Info:")
print(df.info())

# Convert all column names to lowercase for consistency
df.columns = df.columns.str.lower().str.strip()

# Drop rows with missing essential columns
essential_columns = ["job title", "skills"]
df = df.dropna(subset=essential_columns)

# Handle duplicate entries if any
df = df.drop_duplicates()

# Convert date column to datetime format
if "job posting date" in df.columns:
    df["job posting date"] = pd.to_datetime(df["job posting date"], errors="coerce")

# Save processed data
df.to_csv(output_path, index=False)

print("\n✅ Preprocessing complete!")
print(f"📂 Processed file saved at: {output_path}")
print(f"📊 Final Dataset Shape: {df.shape}")
