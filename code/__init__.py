from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_heisman_data():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.heisman.com")

        # Example: Scrape year, player, and school
        data = []
        rows = page.query_selector_all(".winner-table-row")
        for row in rows:
            year = row.query_selector(".year").inner_text()
            player = row.query_selector(".player").inner_text()
            school = row.query_selector(".school").inner_text()
            data.append([year, player, school])

        browser.close()
        df = pd.DataFrame(data, columns=["Year", "Player", "School"])
        df.to_csv("data/heisman_data.csv", index=False)

def clean_data(file_path):
    df = pd.read_csv(file_path)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(inplace=True)
    return df

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium

def plot_school_distribution(df):
    st.write('## Bar Plot of Heisman Winners by School')
    st.caption("This plot shows the number of Heisman winner by school.")
    sort_option = st.selectbox('Sort Schools By:', ["Count (Descending)", "Alphabetical"], key="school_sort")
    if sort_option:
        if sort_option == "Count (Descending)":
            school_order = df["School"].value_counts().index
        else:
            school_order = sorted(df["School"].unique())
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x="School", order=school_order, ax=ax)
        ax.set_title("Number of Heisman Winners by School")
        ax.set_xlabel("School")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

def plot_school_distribution(df):
    map_center = [39.5, -98.35]
    map_ = folium.Map(location=map_center, zoom_start=5)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            popup=f"{row['Player']} ({row['Year']})",
            tooltip=row['School'],
            icon=folium.Icon(color="blue")
        ).add_to(map_)
    st.wrtie("### Folium Map Showing Heisman winners Schools and Players")
    st_data = sf.st_folium(map_, width=725)
    st.write(st_data)

st.title("Heisman Winners Dashboard")
df = clean_data("data/heisman_data.csv")
st.dataframe(df)
year = st.selectbox("Select Year", options=sorted(df["Year"].unique()))
filtered_df = df[df["Year"] == year]
st.write(filtered_df)
st.subheader("Number of Winners by School")
plot_school_distribution(df)