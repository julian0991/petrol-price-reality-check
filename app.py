
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="The Petrol Price Reality Check",
    page_icon="⛽",
    layout="centered"
)

DATA = Path(__file__).resolve().parent / "data"


@st.cache_data
def load_data():
    stations = pd.read_csv(
        DATA / "latest_station_prices.csv",
        dtype={
            "site_id": "string",
            "postcode_standard": "string"
        }
    )

    stations["timestamp"] = pd.to_datetime(
        stations["timestamp"],
        utc=True
    )

    return stations


stations = load_data()

reference_time = stations["timestamp"].max()
total_stations = len(stations)
older_prices = (stations["age_days"] > 7).sum()
older_percentage = older_prices / total_stations * 100

st.caption("THE TIMES | DATA INTERACTIVE")

st.title("The Petrol Price Reality Check")

st.markdown(
    "### The cheapest petrol near you might not be what it seems"
)

st.write(
    "Find reported E10 petrol prices near you, compare potential "
    "savings and see when each station last updated its price."
)

st.divider()

st.metric(
    label="Stations with prices more than seven days old",
    value=f"{older_percentage:.1f}%",
    help="Measured against the extract's latest timestamp."
)

st.write(
    f"Of {total_stations:,} stations with usable matched prices, "
    f"{older_prices:,} had last reported a price more than seven days "
    "before the extract's reference time."
)

st.caption(
    "Source: UK Government Fuel Finder data supplied for the assessment. "
    f"Reference: {reference_time.strftime('%d %B %Y, %H:%M UTC')}. "
    "This is a historical snapshot, not a live price feed."
)

st.divider()

st.subheader("Find petrol prices in your area")

st.write(
    "Enter a UK postcode district to compare stations in the same "
    "district. Prices are from the supplied historical snapshot."
)

district = st.text_input(
    "Postcode district",
    placeholder="e.g. SW1, HG1, M1"
).strip().upper()

if district:
    local = stations.loc[
        stations["postcode_outward"] == district
    ].copy()

    if local.empty:
        st.warning(
            "No stations found for this postcode district. "
            "Check the district or try another."
        )

    else:
        st.write(
            f"Found **{len(local)} stations** with reported E10 prices "
            f"in postcode district **{district}**."
        )

        fresh_only = st.toggle(
            "Show only prices reported within 7 days",
            value=False
        )

        if fresh_only:
            comparison = local.loc[
                local["age_days"] <= 7
            ].copy()
        else:
            comparison = local.copy()

        excluded_count = len(local) - len(comparison)

        if fresh_only:
            st.caption(
                f"{excluded_count} older price reports hidden. "
                "The seven-day threshold is measured against "
                "the dataset's reference timestamp."
            )

        if comparison.empty:
            st.warning(
                "No stations in this district have prices reported "
                "within seven days of the snapshot."
            )

        else:
            comparison = comparison.sort_values(
                ["price_ppl", "age_days"]
            )

            cheapest = comparison.iloc[0]
            most_expensive = comparison.iloc[-1]

            saving_50l = (
                most_expensive["price_ppl"]
                - cheapest["price_ppl"]
            ) * 0.5

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Lowest reported price",
                    f"{cheapest['price_ppl']:.1f}p/L"
                )

            with col2:
                st.metric(
                    "Potential saving on 50L",
                    f"£{saving_50l:.2f}"
                )

            st.caption(
                f"Based on {len(comparison)} stations. The potential "
                "saving compares the lowest and highest reported prices "
                "in this district. It excludes travel costs and does "
                "not guarantee current pump prices."
            )

            comparison["price_age"] = comparison["age_days"].apply(
                lambda age: (
                    "Within 7 days"
                    if age <= 7
                    else f"{age:.0f} days old"
                )
            )

            comparison["last_reported"] = (
                comparison["timestamp"]
                .dt.strftime("%d %b %Y")
            )

            st.subheader("Station details")

            for _, station in comparison.iterrows():
                with st.container(border=True):
                    st.markdown(
                        f"**{station['trading_name']}**"
                    )

                    st.markdown(
                        f"### {station['price_ppl']:.1f}p/L"
                    )

                    if station["age_days"] <= 7:
                        st.caption(
                            "🟢 Reported within 7 days"
                        )
                    else:
                        st.caption(
                            f"🟠 Reported {station['age_days']:.0f} "
                            "days before the snapshot"
                        )

                    st.caption(
                        f"Postcode: {station['postcode_standard']} · "
                        f"Last reported: {station['last_reported']}"
                    )

            st.subheader("How do local prices compare?")

            chart_data = comparison.copy()

            chart_data["Reporting age"] = chart_data[
                "age_days"
            ].apply(
                lambda days: (
                    "Reported within 7 days"
                    if days <= 7
                    else "Older than 7 days"
                )
            )

            chart_data["Station"] = chart_data["trading_name"]
            chart_data["Price (p/L)"] = (
                chart_data["price_ppl"].round(1)
            )

            # Short labels keep the chart readable on narrow screens.
            chart_data["Station label"] = (
                chart_data["Station"]
                .astype(str)
                .str.slice(0, 18)
            )

            # Give duplicate names distinct labels.
            chart_data["Station label"] = (
                chart_data["Station label"]
                + " · "
                + chart_data["postcode_standard"].fillna("")
            )

            chart_data = chart_data.sort_values(
                "Price (p/L)",
                ascending=False
            )

            fig = px.scatter(
                chart_data,
                x="Price (p/L)",
                y="Station label",
                color="Reporting age",
                text="Price (p/L)",
                color_discrete_map={
                    "Reported within 7 days": "#26796f",
                    "Older than 7 days": "#d97745"
                },
                hover_name="Station",
                hover_data={
                    "age_days": ":.1f",
                    "Price (p/L)": ":.1f",
                    "Station label": False
                }
            )

            fig.update_traces(
                marker=dict(size=13),
                texttemplate="%{text:.1f}p",
                textposition="top center",
                textfont=dict(size=11)
            )

            fig.update_layout(
                height=max(340, len(chart_data) * 65),
                margin=dict(l=0, r=5, t=35, b=10),
                showlegend=False,
                yaxis_title=None,
                xaxis_title="Price (p/L)"
            )

            fig.update_yaxes(
                automargin=True,
                showgrid=True,
                gridcolor="#e5e7eb"
            )

            fig.update_xaxes(
                range=[
                    chart_data["Price (p/L)"].min() - 2,
                    chart_data["Price (p/L)"].max() + 2
                ],
                ticksuffix="p"
            )

            st.caption(
                "🟢 Reported within 7 days   "
                "🟠 Older than 7 days"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.caption(
                "Dots show the latest usable E10 price for each station. "
                "Reporting age is measured against 1 October 2026. "
                "An older observation is not necessarily inaccurate."
            )

            
