# bbcc4

Exploring the BBC News subset of the C4 dataset (via allenai/c4's realnewslike subset on HF),
originally a Google dataset

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
