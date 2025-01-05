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
