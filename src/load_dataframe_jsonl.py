import polars as pl

df = pl.read_json(
    "hf://datasets/allenai/c4/realnewslike/c4-train.00000-of-00512.json.gz",
    schema=["timestamp", "url"],
)
