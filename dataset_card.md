---
dataset_info:
  config_name: realnewslike-bbc-news
  features:
  - name: url
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: train
    num_bytes: 215860989
    num_examples: 77481
  download_size: 133287879
  dataset_size: 215860989
configs:
- config_name: realnewslike-bbc-news
  data_files:
  - split: train
    path: realnewslike-bbc-news/train-*
license: odc-by
language:
- en
pretty_name: BBC News from C4
size_categories:
- 10K<n<100K
---

# Dataset Card for BBC News from C4

This dataset provides a filtered subset of BBC News articles from the realnewslike subset of the C4 dataset, containing approximately 77k articles from BBC News domains.

## Dataset Details

### Dataset Description

- **Curated by:** Louis Maddox (@permutans on HuggingFace and X/Twitter)
- **License:** ODC-BY (inherited from C4)
- **Language:** English

### Dataset Sources
- **Repository:** https://huggingface.co/datasets/permutans/c4-bbc-news
- **Source Dataset:** allenai/c4 (realnewslike subset)
- **Paper:** https://arxiv.org/abs/1910.10683 (C4 paper)

## Uses

### Direct Use
Suitable for text analysis and NLP tasks focused on news content, particularly when working with BBC News articles. The dataset provides cleaned article text without metadata like bylines or publication dates.

### Out-of-Scope Use
This dataset should not be used as a comprehensive archive of BBC News content, as it represents only articles captured in C4's crawl around 2019. It should not be assumed to contain all articles from any given time period.

## Dataset Structure

### Data Instances
Example format:
```python
{
    'url': 'news.bbc.co.uk/news/article-path',
    'text': 'Article content...'
}
```

### Data Fields
- `url`: URL of the article with query parameters removed 
- `text`: Full article text content

### Data Statistics
- Contains approximately 77k articles
- No validation split in current version

## Dataset Creation

### Curation Rationale
Created to provide an easily accessible dataset of BBC news articles while offering a focused view into the C4 dataset's coverage of major news sources. Enables analysis of C4's completeness and motivates investigation of alternative data acquisition methods.

### Source Data
#### Data Collection and Processing
- Filtered from C4's realnewslike subset
- Limited to domains: news.bbc.co.uk, www.bbc.co.uk/news, www.bbc.com/news
- URL cleaning: removed query parameters
- Regional news content excluded due to sparse coverage in source data
- No modifications to article text content

#### Personal and Sensitive Information
Article texts contain only the main content body, without bylines or metadata.

## Bias, Risks, and Limitations

- No validation split in current version
- Original publication dates not available (C4 timestamps were crawl dates)
- Section/index pages not yet filtered out from article pages
- Regional news content explicitly excluded due to sparse coverage
- Relationship between news.bbc.co.uk and bbc.co.uk/news domains needs investigation
- Coverage may be incomplete compared to full BBC News archive

### Recommendations
Users should be aware that this represents a subset of BBC News content which appears to be from around 2019 and earlier. For applications requiring comprehensive coverage or accurate publication dates, additional data sources should be considered.

## Future Directions
- Potential expansion using fineweb dataset for more recent content
- Addition of publication dates through targeted crawling
- Filtering to distinguish between section pages and article pages
- Creation of validation split

## Citation
Please cite the original C4 dataset when using this data. A reference to this one would be welcome but not necessary, I consider this a derivative work.

## Dataset Card Authors
Louis Maddox (@permutans)
