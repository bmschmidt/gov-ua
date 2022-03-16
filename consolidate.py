import pyarrow as pa
from pathlib import Path
from pyarrow import parquet as pq
from pyarrow import compute as pc

def main():
  fs = []

  for file in Path("parquet/").glob("*.parquet"):
    r = pq.read_table(file)
    fs.append(r.select(['time', 'url', 'ip', 'status', 'run', 'error']))

  combined = pa.concat_tables(tables=fs)
  combined = combined.take(pc.sort_indices(combined, sort_keys = [('time', 'ascending')]))
  pq.write_table(combined, "sucho_status.parquet")

if __name__ == "__main__":
  print("Running")
  main()