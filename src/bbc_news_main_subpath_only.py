from pprint import pprint

import polars as pl
from huggingface_hub import hf_hub_url, list_repo_files
from tqdm import tqdm

file_names = pl.Series(list_repo_files("allenai/c4", repo_type="dataset"))
# Take all splits of the realnewslike subset (513 files)
news_files = file_names.filter(
    file_names.str.starts_with("realnewslike/") & file_names.str.ends_with(".json.gz"),
).str.strip_prefix("realnewslike/")

c4n_features = {"url": pl.String, "text": pl.String}
aggregator = pl.DataFrame(schema=c4n_features)

domain_capture = r"https?://([^/?]+)"
subpage_capture = r"https?://[^/]+(\/[^/?]+\/)"  # Include pre/suffix slashes
url_match = r"^(news\.bbc\.co\.uk|www\.bbc\.co\.uk|www\.bbc\.com)$"
allowed_subpages = pl.DataFrame({"path": ["/news/"]})  # No regions
path_col = pl.col("url").str.extract(subpage_capture)

for filename in tqdm(news_files):
    json_url = hf_hub_url(
        repo_id="allenai/c4",
        filename=filename,
        subfolder="realnewslike",
        repo_type="dataset",
    )
    print(f"Processing {json_url}")
    df = (
        pl.read_ndjson(json_url, schema=c4n_features)
        .with_columns(pl.col("url").str.extract(r"([^?]+)"))
        .filter(
            pl.col("url").str.extract(domain_capture).str.contains(url_match),
            ~pl.col("url").str.contains(r"https?://[^/]+\/\?"),  # Path is a ?
        )
    )
    # Just match the "/news/" path here
    news_df = df.filter(path_col == "/news/")
    aggregator = pl.concat([aggregator, news_df])
    print(aggregator)
