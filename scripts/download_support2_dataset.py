from ucimlrepo import fetch_ucirepo
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent
data_dir = scripts_dir.parent / "data"

data_dir.mkdir(parents=True, exist_ok=True)
file_path = data_dir / "support2_complete.csv"

support2 = fetch_ucirepo(id=880)
# Pull the complete original dataframe (this includes Features, Targets, IDs, and 'Other' roles)
df_complete = support2.data.original
df_complete.to_csv(file_path, index=False)

print(f"Dataset saved with all {df_complete.shape[1]} columns!")
