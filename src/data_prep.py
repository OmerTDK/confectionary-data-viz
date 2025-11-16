#!/usr/bin/env python3
"""
Data preparation module for the Confectionary Sales Dashboard
Contains all data cleaning, feature engineering, and aggregation functions
"""

import pandas as pd
import numpy as np
from typing import Tuple


def load_and_clean_data(filepath: str = "confectionary.xlsx") -> pd.DataFrame:
    """
    Load confectionary data and apply initial cleaning steps

    Args:
        filepath: Path to the Excel file

    Returns:
        Cleaned pandas DataFrame
    """
    # Load data
    df = pd.read_excel(filepath)

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Drop rows with missing dates
    df = df.dropna(subset=["Date"])

    # Clean numeric columns
    numeric_cols = ["Units Sold", "Cost(£)", "Profit(£)", "Revenue(£)"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Drop rows with missing numeric values
    df = df.dropna(subset=numeric_cols)

    # Remove rows with non-positive units sold or revenue
    df = df[(df["Units Sold"] > 0) & (df["Revenue(£)"] > 0)]

    return df


def normalize_confectionary_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix spelling variations in confectionary names

    Args:
        df: Input DataFrame with Confectionary column

    Returns:
        DataFrame with normalized confectionary names
    """
    conf_mapping = {
        "Choclate Chunk": "Chocolate Chunk",
        "Caramel nut": "Caramel Nut",
        # Add any additional variants discovered
    }

    df = df.copy()
    df["Confectionary_clean"] = df["Confectionary"].replace(conf_mapping)
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features to the DataFrame

    Args:
        df: Input DataFrame with Date column

    Returns:
        DataFrame with additional time features
    """
    df = df.copy()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%b")
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    return df


def add_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add financial ratio and per-unit metrics

    Args:
        df: Input DataFrame with financial columns

    Returns:
        DataFrame with additional financial features
    """
    df = df.copy()
    df["Profit_Margin"] = df["Profit(£)"] / df["Revenue(£)"]
    df["Revenue_per_Unit"] = df["Revenue(£)"] / df["Units Sold"]
    df["Cost_per_Unit"] = df["Cost(£)"] / df["Units Sold"]
    df["Profit_per_Unit"] = df["Profit(£)"] / df["Units Sold"]
    return df


def prepare_data(filepath: str = "confectionary.xlsx") -> pd.DataFrame:
    """
    Complete data preparation pipeline

    Args:
        filepath: Path to the Excel file

    Returns:
        Fully prepared DataFrame with all features
    """
    # Load and clean
    df = load_and_clean_data(filepath)

    # Normalize names
    df = normalize_confectionary_names(df)

    # Add time features
    df = add_time_features(df)

    # Add financial features
    df = add_financial_features(df)

    return df


def get_regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create regional performance summary

    Args:
        df: Prepared DataFrame

    Returns:
        Regional summary DataFrame
    """
    regional_summary = df.groupby("Country(UK)", as_index=False).agg({
        "Units Sold": "sum",
        "Revenue(£)": "sum",
        "Profit(£)": "sum"
    })

    regional_summary["Profit_Margin"] = (
        regional_summary["Profit(£)"] / regional_summary["Revenue(£)"]
    )

    return regional_summary


def get_product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create confectionary product performance summary

    Args:
        df: Prepared DataFrame

    Returns:
        Product summary DataFrame
    """
    conf_summary = df.groupby("Confectionary_clean", as_index=False).agg({
        "Units Sold": "sum",
        "Revenue(£)": "sum",
        "Profit(£)": "sum"
    })

    conf_summary["Profit_Margin"] = (
        conf_summary["Profit(£)"] / conf_summary["Revenue(£)"]
    )

    return conf_summary


def get_regional_product_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create region × product profit margin matrix

    Args:
        df: Prepared DataFrame

    Returns:
        Pivot table with profit margins
    """
    region_conf = df.groupby(
        ["Country(UK)", "Confectionary_clean"], as_index=False
    ).agg({
        "Units Sold": "sum",
        "Revenue(£)": "sum",
        "Profit(£)": "sum"
    })

    region_conf["Profit_Margin"] = (
        region_conf["Profit(£)"] / region_conf["Revenue(£)"]
    )

    return region_conf


def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create monthly sales trends by region

    Args:
        df: Prepared DataFrame

    Returns:
        Monthly trends DataFrame
    """
    monthly_region = df.groupby(
        [pd.Grouper(key="Date", freq="M"), "Country(UK)"],
        as_index=False
    )["Units Sold"].sum()

    return monthly_region
