# bbcc4

Exploring the BBC News subset of the C4 dataset (via allenai/c4's realnewslike subset on HF),
originally a Google dataset

1. Timestamps
2. BBC news articles

## Timestamps

A cursory look at the timestamps, topping and tailing each file in the realnewsfiles subset, shows
they were all in the period from 2019-04-18 to 2019-04-26 apart from a couple outliers dating back to 2013 and 2014:

- See `src/date_top_tail.py` for source

```
>>> aggregator.sort("timestamp")
shape: (1_026, 2)
┌─────────────────────┬─────────────────────────────────┐
│ timestamp           ┆ url                             │
│ ---                 ┆ ---                             │
│ datetime[μs]        ┆ str                             │
╞═════════════════════╪═════════════════════════════════╡
│ 2013-03-05 16:57:00 ┆ http://www.cnn.com/             │
│ 2014-08-02 09:52:13 ┆ http://news.bbc.co.uk/2/hi/afr… │
│ 2019-04-18 10:13:36 ┆ http://shopping.rediff.com/pro… │
│ 2019-04-18 10:13:37 ┆ http://vibeghana.com/2010/11/0… │
│ 2019-04-18 10:13:40 ┆ https://www.inman.com/2010/02/… │
│ …                   ┆ …                               │
│ 2019-04-26 17:33:26 ┆ https://www.chicagotribune.com… │
│ 2019-04-26 17:33:30 ┆ https://www.chicagotribune.com… │
│ 2019-04-26 17:33:33 ┆ https://www.chicagotribune.com… │
│ 2019-04-26 17:33:43 ┆ https://www.chicagotribune.com… │
│ 2019-04-26 17:33:46 ┆ https://www.chicagotribune.com… │
└─────────────────────┴─────────────────────────────────┘
```

Taking aggregate counts per year, it turns out these are in fact two lone outliers, and not
indicative of any distribution stretching back to 2013 (out of a total 13.8M rows)

- See `src/date_year_agg.py` for source

```
┌──────────┬──────┬──────┐
│ 2019     ┆ 2013 ┆ 2014 │
│ ---      ┆ ---  ┆ ---  │
│ i64      ┆ i64  ┆ i64  │
╞══════════╪══════╪══════╡
│ 13813699 ┆ 1    ┆ 1    │
└──────────┴──────┴──────┘
```

Note that this means the timestamp can be dropped, it is not informative about anything apart from
when the scrape was ran (I presume). There is no paper from Google or AllenAI about this dataset to
my knowledge to document it either way.

## BBC news articles

The BBC news website has changed where articles live a few times, so it's best to just match on
the `bbc.co.uk` substring initially.

- See `bbc_urls.py` for source

There are 91,361 sites in `realnewslike` with `bbc.co.uk/` in the URL, presumably all are BBC News.

```
shape: (91_361, 1)
┌─────────────────────────────────┐
│ url                             │
│ ---                             │
│ str                             │
╞═════════════════════════════════╡
│ https://www.bbc.co.uk/news/ent… │
│ http://www.bbc.co.uk/bristol/i… │
│ https://www.bbc.co.uk/news/av/… │
│ https://www.bbc.co.uk/news/av/… │
│ https://www.bbc.co.uk/news/sci… │
│ …                               │
│ http://news.bbc.co.uk/sport2/h… │
│ https://www.bbc.co.uk/news/uk-… │
│ https://www.bbc.co.uk/mediacen… │
│ http://news.bbc.co.uk/2/hi/823… │
│ https://www.bbc.co.uk/news/sci… │
└─────────────────────────────────┘
```

If we break out the domains...

<details><summary>Click to show</summary>

```py
>>> domain_capture = r"https?://([^/?]+)"
>>> pprint(aggregator.sort("url")["url"].str.extract(domain_capture).unique().to_list())
['archiveservices.tools.bbc.co.uk',
 'bbcthree-web-server.api.bbc.co.uk',
 'careershub.bbc.co.uk',
 'careerssearch.bbc.co.uk',
 'ethics.virt.ch.bbc.co.uk',
 'genome.ch.bbc.co.uk',
 'hevc.kw.bbc.co.uk',
 'news.bbc.co.uk',
 'newsbeat-explains.ch.bbc.co.uk',
 'peakyblinders.ch.bbc.co.uk',
 'react.ch.bbc.co.uk',
 'support.bbc.co.uk',
 'swap.stanford.edu',
 'thira.ch.bbc.co.uk',
 'waveform.prototyping.bbc.co.uk',
 'webaudio.prototyping.bbc.co.uk',
 'writersroom.external.bbc.co.uk',
 'wscareerssearch.bbc.co.uk',
 'www.bbc.co.uk',
 'www.bbc.com',
 'www.reuters.com']
```

</details>

We see that there are only 3 valid BBC domains:

- 'news.bbc.co.uk'
- 'www.bbc.co.uk'
- 'www.bbc.com'

This leads to a simple regex through which we arrive at the proper filtered subset of 147,546 BBC URLs
(which we expect in this `realnewslike` subset to be entirely news, hence to be entirely BBC News).

```
shape: (147_546, 1)
┌─────────────────────────────────┐
│ url                             │
│ ---                             │
│ str                             │
╞═════════════════════════════════╡
│ https://www.bbc.com/sport/foot… │
│ https://www.bbc.co.uk/news/ent… │
│ http://www.bbc.co.uk/bristol/i… │
│ https://www.bbc.co.uk/news/av/… │
│ https://www.bbc.com/sport/foot… │
│ …                               │
│ https://www.bbc.co.uk/mediacen… │
│ https://www.bbc.com/news/techn… │
│ http://news.bbc.co.uk/2/hi/823… │
│ https://www.bbc.co.uk/news/sci… │
│ https://www.bbc.com/news/world… │
└─────────────────────────────────┘
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 513/513 [01:36<00:00,  5.31it/s]
Domains: ['news.bbc.co.uk', 'www.bbc.co.uk', 'www.bbc.com']
```

We can further filter out the sports articles as being BBC Sport, taking out a third of the rows:

```
>>> aggregator.filter(~pl.col("url").str.contains("/sport/"))
shape: (105_494, 1)
>>> aggregator.filter(pl.col("url").str.contains("/sport/"))
shape: (42_052, 1)
```

(Lastly I added back the `text` column to the schema)

```
>>> aggregator
shape: (105_494, 2)
┌─────────────────────────────────┬─────────────────────────────────┐
│ url                             ┆ text                            │
│ ---                             ┆ ---                             │
│ str                             ┆ str                             │
╞═════════════════════════════════╪═════════════════════════════════╡
│ https://www.bbc.co.uk/news/ent… ┆ The Rolling Stones' US tour is… │
│ http://www.bbc.co.uk/bristol/i… ┆ Take a look around the Nationa… │
│ https://www.bbc.co.uk/news/av/… ┆ Hands-on with a transparent 3D… │
│ https://www.bbc.co.uk/news/av/… ┆ Meet The Author: Robyn Young J… │
│ https://www.bbc.co.uk/news/sci… ┆ The "Pandora's box" of unmanne… │
│ …                               ┆ …                               │
│ https://www.bbc.co.uk/mediacen… ┆ I play Aubrey, who is a very f… │
│ https://www.bbc.com/news/techn… ┆ Mobile phones could soon be he… │
│ http://news.bbc.co.uk/2/hi/823… ┆ Startled pigeons might not app… │
│ https://www.bbc.co.uk/news/sci… ┆ The tail of a feathered dinosa… │
│ https://www.bbc.com/news/world… ┆ Rival protests over a murder i… │
└─────────────────────────────────┴─────────────────────────────────┘
```

## BBC News URLs

> See `src/bbc_news_urls.py` for source

Breaking down the URLs by the first path part after the domain (just "path"), there's a lot of
non-news articles (the 2nd most common by frequency is `/blogs/` which didn't strike me as news
so much as news-adjacent). I identified all of the regional paths and put them aside (included).

This gives about 45 thousand BBC News items in C4, with no metadata on the year of publication.

```py
>>> aggregator
shape: (44_588, 2)
┌─────────────────────────────────┬─────────────────────────────────┐
│ url                             ┆ text                            │
│ ---                             ┆ ---                             │
│ str                             ┆ str                             │
╞═════════════════════════════════╪═════════════════════════════════╡
│ http://www.bbc.co.uk/bristol/i… ┆ Take a look around the Nationa… │
│ https://www.bbc.co.uk/news/ent… ┆ The Rolling Stones' US tour is… │
│ https://www.bbc.co.uk/news/av/… ┆ Hands-on with a transparent 3D… │
│ https://www.bbc.co.uk/news/av/… ┆ Meet The Author: Robyn Young J… │
│ https://www.bbc.co.uk/news/sci… ┆ The "Pandora's box" of unmanne… │
│ …                               ┆ …                               │
│ https://www.bbc.com/news/av/wo… ┆ World Trade Center build at ha… │
│ https://www.bbc.co.uk/news/uk-… ┆ Image caption William Alldis r… │
│ https://www.bbc.com/news/techn… ┆ Mobile phones could soon be he… │
│ https://www.bbc.co.uk/news/sci… ┆ The tail of a feathered dinosa… │
│ https://www.bbc.com/news/world… ┆ Rival protests over a murder i… │
└─────────────────────────────────┴─────────────────────────────────┘
```

It's proportionally about 99% `/news/` in the remainder with a long tail of regional content, which
could be omitted for simplicity.

```py
>>> with pl.Config() as cfg:                                                                                                
...     cfg.set_tbl_rows(-1)                                                                                                
...     aggregator.with_columns(path_col)["path"].value_counts().sort("count", descending=True).with_row_index().pipe(print)                                                                                   
... 
<class 'polars.config.Config'>
shape: (48, 3)
┌───────┬────────────────────────┬───────┐
│ index ┆ path                   ┆ count │
│ ---   ┆ ---                    ┆ ---   │
│ u32   ┆ str                    ┆ u32   │
╞═══════╪════════════════════════╪═══════╡
│ 0     ┆ /news/                 ┆ 43965 │
│ 1     ┆ /wales/                ┆ 153   │
│ 2     ┆ /scotland/             ┆ 49    │
│ 3     ┆ /northernireland/      ┆ 40    │
│ 4     ┆ /cornwall/             ┆ 30    │
│ 5     ┆ /southyorkshire/       ┆ 19    │
│ 6     ┆ /cumbria/              ┆ 18    │
│ 7     ┆ /bristol/              ┆ 17    │
│ 8     ┆ /suffolk/              ┆ 16    │
│ 9     ┆ /stoke/                ┆ 16    │
│ 10    ┆ /shropshire/           ┆ 15    │
│ 11    ┆ /gloucestershire/      ┆ 15    │
│ 12    ┆ /wiltshire/            ┆ 15    │
│ 13    ┆ /leicester/            ┆ 14    │
│ 14    ┆ /nottingham/           ┆ 14    │
│ 15    ┆ /leeds/                ┆ 13    │
│ 16    ┆ /devon/                ┆ 12    │
│ 17    ┆ /birmingham/           ┆ 11    │
│ 18    ┆ /bradford/             ┆ 11    │
│ 19    ┆ /norfolk/              ┆ 10    │
│ 20    ┆ /manchester/           ┆ 9     │
│ 21    ┆ /london/               ┆ 9     │
│ 22    ┆ /coventry/             ┆ 9     │
│ 23    ┆ /liverpool/            ┆ 8     │
│ 24    ┆ /jersey/               ┆ 8     │
│ 25    ┆ /cambridgeshire/       ┆ 8     │
│ 26    ┆ /readingandleeds/      ┆ 7     │
│ 27    ┆ /dorset/               ┆ 7     │
│ 28    ┆ /england/              ┆ 7     │
│ 29    ┆ /herefordandworcester/ ┆ 6     │
│ 30    ┆ /hampshire/            ┆ 6     │
│ 31    ┆ /berkshire/            ┆ 5     │
│ 32    ┆ /northamptonshire/     ┆ 5     │
│ 33    ┆ /tyne/                 ┆ 5     │
│ 34    ┆ /kent/                 ┆ 4     │
│ 35    ┆ /derby/                ┆ 4     │
│ 36    ┆ /essex/                ┆ 3     │
│ 37    ┆ /chelsea/              ┆ 3     │
│ 38    ┆ /lancashire/           ┆ 3     │
│ 39    ┆ /somerset/             ┆ 3     │
│ 40    ┆ /tees/                 ┆ 3     │
│ 41    ┆ /lincolnshire/         ┆ 3     │
│ 42    ┆ /blackcountry/         ┆ 3     │
│ 43    ┆ /humber/               ┆ 2     │
│ 44    ┆ /oxford/               ┆ 2     │
│ 45    ┆ /isleofman/            ┆ 1     │
│ 46    ┆ /southampton/          ┆ 1     │
│ 47    ┆ /guernsey/             ┆ 1     │
└───────┴────────────────────────┴───────┘
```

## BBC News drill down

> See `src/bbc_news_main_subpath_only.py`

To just look at the URLs of the subset identified under `/news/` in the last section

A quick way to get a look inside the remainder is to see how many subpaths deep they go:

```py
# First extract everything before any query parameters
patterns = aggregator.select(
    pl.col("url").str.extract(r"https?://[^/]+/news/([^?]+)").alias("path_structure")
).with_columns([
    pl.col("path_structure").str.count_matches("/").alias("slash_count"),
])
```

When we look at these, there are still evidently oddities that aren't news articles:

> This result for example is some sort of fragment from a school leaderboard.

```py
>>> patterns["slash_count"].max()                                                                                                                                                                                   
6
>>> patterns.filter(pl.col("slash_count") == 6)[0].to_dicts()
[{'path_structure': 'special/education/school_tables/primary/10/html/868.stm', 'slash_count': 6, 'is_numeric': False, 'is_world': False, 'is_uk': False, 'is_av': False}]
>>> pprint(aggregator.filter(pl.col("url").str.contains("special/education/school_tables/primary/10/html/868.stm")).to_dicts())
[{'text': '% achieving L4 maths and Eng What does this mean?\n'
          'Average point score What does this mean?\n'
          'Contextual value added What does this mean?',
  'url': 'http://www.bbc.co.uk/news/special/education/school_tables/primary/10/html/868.stm'}]
```

It's easier to interpret the path structure here as "levels" (non-leaf path parts), and counting
them/taking unique values with examples:

<details><summary>Click to show:</summary>

```py
pl.Config.set_tbl_rows(-1)
pl.Config.set_tbl_width(-1)
pl.Config(fmt_str_lengths=1000)

level_patterns = (patterns
   .group_by(["level1", "level2", "rest"])
   .agg([
       pl.len().alias("count"),
       pl.first("example_url").alias("example")
   ])
   .with_columns([
       pl.concat_str([
           pl.coalesce(pl.col("level1"), pl.lit("")),
           pl.coalesce(pl.col("level2"), pl.lit("")),
           pl.coalesce(pl.col("rest"), pl.lit(""))
       ], separator="/").alias("path_order"),
       # Count the number of non-null path components
       (pl.col("level1").is_not_null().cast(pl.Int32) + 
        pl.col("level2").is_not_null().cast(pl.Int32) + 
        pl.col("rest").is_not_null().cast(pl.Int32)).alias("path_depth")
   ])
   .sort("path_order")
)
```

</details>

This gives a very large number of patterns to begin working away at (a pager would help here, like
`str(list()) around `pydoc.pager``).

```py
from pydoc import pager
from pprint import pformat, pprint

def listpager(l):
    pager("\n".join([i if type(i) is str else repr(i) for i in l]))
```

...so as to whittle away the non-useful subsets - ideally there would be only a handful of formats
for standalone articles' URLs!
