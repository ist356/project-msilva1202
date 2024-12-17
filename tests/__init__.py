from code.scraper import scrape_heisman_data
import os

def test_scrape_heisman_data():
    scrape_heisman_data()
    assert os.path.exists("data/heisman_data.csv")

from code.data_processing import clean_data

def test_clean_data():
    df = clean_data("data/sample.csv")
    assert not df.empty
    assert "Year" in df.columns
    assert "Player" in df.columns
    assert "School" in df.columns

from code.visualizations import plot_school_distribution
import pandas as pd

def test_plot_school_distribution():
    df = pd.DataFrame({
        "School": ["Alabama", "LSU", "Alabama", "Ohio State"]
    })
    try:
        plot_school_distribution(df)
    except Exception as e:
        assert False, f"Plotting failed with error: {e}"