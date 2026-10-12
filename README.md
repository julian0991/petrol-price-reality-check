# The Petrol Price Reality Check

**A mobile-first data journalism project exploring UK petrol prices and how recently they were reported.**

Developed as part of the Data Developer recruitment assessment for The Times and The Sunday Times.

## The editorial question

**Where can readers find the cheapest reported E10 petrol in their area, and how recently was that price updated?**

The lowest reported price is not always the most useful if it has not been updated recently. This project lets readers compare petrol stations while seeing when each price was last reported.

## The key finding

**Nearly one in three petrol stations (32.9%) had a reported price more than seven days old in the supplied dataset.**

Of the 7,937 stations with usable prices and matching station information, 2,613 had not reported a newer price within seven days of the dataset's reference timestamp.

This finding emerged during data exploration and cleaning. It became the basis for the interactive because price alone does not tell readers how recent the information is.

An older reported price is not necessarily incorrect, but it gives readers less recent evidence of what they might pay at the pump.

## What the interactive does

- Searches for petrol stations by UK postcode district.
- Compares reported E10 petrol prices at stations in the selected district.
- Calculates the potential saving on a 50-litre fill-up.
- Lets readers compare all reported prices with those updated within seven days of the dataset snapshot.
- Displays station names, prices, reporting dates and an interactive price comparison chart.
- Uses a mobile-friendly layout designed for quick comparisons.

The application was built using **Python, pandas, Streamlit and Plotly**.

## Data and methodology

The project uses UK Government Fuel Finder data supplied for the assessment, including E10 petrol price histories and petrol station information.

The original datasets contained **347,612 price observations** and **8,148 station records**.

Initial data exploration identified several issues:

- 116 price observations outside the provisional 100–250p/L review range.
- Nine unusually low prices with corresponding pence values recorded at the same station and timestamp, suggesting inconsistent price units.
- Four unusually old timestamps dating from before 2026.
- Missing country, county and postcode information.
- Inconsistent country names and postcode formatting.
- 88 station IDs in the price history without matching station information.

Rather than automatically removing or correcting questionable records, the original data was preserved and the issues investigated before defining the cleaning rules.

Country names and postcode formats were standardised in separate fields. Missing geographical information was retained where it could not be verified.

Price observations outside the provisional range were flagged rather than automatically converted. January 2026 observations were retained after further investigation showed they accounted for most of the initially flagged older timestamps.

The derived historical analysis dataset contained **347,492 observations**, following the exclusion of 116 price-range anomalies and four pre-2026 timestamps. These exclusions were made for analytical purposes and do not establish that every excluded record was incorrect.

The interactive uses the latest usable E10 price for each station with matching metadata, producing **7,937 station-level records**.

Price freshness is calculated against the latest timestamp in the supplied data: **1 October 2026 at 14:36:48 UTC**.

## Limitations

This project uses a historical snapshot rather than live petrol prices.

The seven-day freshness threshold is measured against the snapshot date, not the current date. Even a recently reported price may have changed since it was recorded.

Searches use postcode districts, so stations shown together are not necessarily within a short driving distance of one another.

The potential saving on a 50-litre fill-up is calculated from the difference between the highest and lowest reported prices in the selected district. It does not account for travel costs or guarantee the price available at the pump.

The price screening rules reduce the impact of unusual observations but cannot establish that every retained record is accurate.

## Project files

- `app.py`: Streamlit application and interactive visualisation.
- `data/latest_station_prices.csv`: Prepared station-level dataset used by the application.
- `requirements.txt`: Python dependencies.

## Running the application locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

## AI assistance

ChatGPT was used to support code review, debugging and documentation, including suggestions during the development process.

## Project purpose

The aim was to build a practical reader-facing tool that combines petrol-price comparisons with information about data freshness.

The analysis showed that reporting age can materially affect local price comparisons. The interactive gives readers the ability to explore that difference themselves, rather than presenting the cheapest reported price without context.

**Live interactive:** https://petrol-price-reality-check.streamlit.app