import polars as pl
import numpy as np  # For generating sample data


# --- Simulate a large CSV file (replace with your actual file) ---
def generate_large_csv(filename, num_rows, num_cols):
    rng = np.random.default_rng(seed=42)  # Use a fixed seed for reproducibility
    data = {f"col_{i}": rng.integers(0, 100, num_rows) for i in range(num_cols)}
    df = pl.DataFrame(data)
    df.write_csv(filename)


filename = "large_data.csv"
num_rows = 20_000_000
num_cols = 10

# generate_large_csv(filename, num_rows, num_cols)
# --- End of simulation ---

# --- Polars: Reading and processing ---
try:
    df = pl.read_csv(filename)

    # Calculate the average of 'col_3' grouped by 'col_1' and 'col_2'
    result = df.group_by(["col_1", "col_2"]).agg(pl.col("col_3").mean())

    print(result)

except pl.exceptions.OutOfMemoryError:
    print(
        "Polars encountered an OutOfMemoryError. Consider optimizing your query or increasing system memory."
    )
except Exception as e:
    print(f"An error occurred: {e}")

# --- Pandas (Demonstration of chunking concept) ---
# import pandas as pd

# chunksize = 1000000  # adjust chunksize according to your RAM.
# results = []

# try:
#     for chunk in pd.read_csv(filename, chunksize=chunksize):
#         if "pandas_results" not in locals():
#             pandas_results = (
#                 chunk.groupby(["col_1", "col_2"])["col_3"].mean().reset_index()
#             )
#         else:
#             pandas_results = pd.concat(
#                 [
#                     pandas_results,
#                     chunk.groupby(["col_1", "col_2"])["col_3"].mean().reset_index(),
#                 ]
#             )

#     final_pandas_results = (
#         pandas_results.groupby(["col_1", "col_2"])["col_3"].mean().reset_index()
#     )
#     print("Pandas chunked results:")
#     print(final_pandas_results)

# except MemoryError:
#     print(
#         "Pandas ran into a memory error. Consider using smaller chunk sizes or Polars."
#     )
# except Exception as e:
#     print(f"Pandas error: {e}")

# --- File Cleanup ---
# import os

# os.remove(filename)  # remove the generated file.
