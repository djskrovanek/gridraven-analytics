from typing import List, Optional, Tuple
import pandas as pd


def filter_and_average(
    start_date: str, 
    end_date: str, 
    time_span: str, 
    tolerance: str,
    FOA_df: pd.DataFrame, 
    Ammonit_df: pd.DataFrame,
    exclude_ranges: Optional[List[Tuple[str, str]]] = None
) -> pd.DataFrame:
    """
    Filters wind data within a date range.
    Applies rolling average over specified time span. (Cigre recommends 10 min)
    Merges data by specifying tolerance for timestamp. (i.e., if tolerance=3 min, then timestamps of 12:10:00 and 12:11:00 are merged)
    Excludes data based on range, if you want (e.g., FOA data from 11/28/24 to 12/5/24 is missing)

    Args:
        start_date: Start of the filtering window (e.g., '2024-11-01').
        end_date: End of the filtering window (e.g., '2025-02-13').
        time_span: Time window for rolling average (e.g., '30min').
        tolerance: Allowable difference in timestamps for merging (e.g., '10min')
        FOA_df: DataFrame containing FOA wind data with a 'Time' column.
        Ammonit_df: DataFrame with Ammonit wind data and a 'datetime' column.
        exclude_ranges: Optional list of (start, end) datetime strings to exclude after interpolation.

    Returns:
        DataFrame of the processed FOA data, Ammonit data, absolute error, and average wind speed of the two.
    """

    # Convert into datetime
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    # Filter and copy data
    FOA_df_filtered = FOA_df[(FOA_df['Time'] >= start_dt) & (FOA_df['Time'] <= end_dt)].copy()
    Ammonit_df_filtered = Ammonit_df[(Ammonit_df['datetime'] >= start_dt) & (Ammonit_df['datetime'] <= end_dt)].copy()

    # Set the datetime column as index
    FOA_df_filtered.set_index('Time', inplace=True)
    Ammonit_df_filtered.set_index('datetime', inplace=True)

    # Apply time-based rolling average
    FOA_df_filtered['wind_m7'] = FOA_df_filtered['wind_m7'].rolling(time_span).mean()
    Ammonit_df_filtered['Avg wind speed'] = Ammonit_df_filtered['Avg wind speed'].rolling(time_span).mean()
    Ammonit_df_filtered['Max wind speed'] = Ammonit_df_filtered['Max wind speed'].rolling(time_span).mean()
    Ammonit_df_filtered['Min wind speed'] = Ammonit_df_filtered['Min wind speed'].rolling(time_span).mean()
    if 'Wind angle' in Ammonit_df_filtered.columns:
        Ammonit_df_filtered['Wind angle'] = Ammonit_df_filtered['Wind angle'].rolling(time_span).mean()


    # Reset index if needed for plotting
    FOA_df_filtered.reset_index(inplace=True)
    Ammonit_df_filtered.reset_index(inplace=True)

    # Create uniform time base
    time_index = pd.date_range(start=start_dt, end=end_dt, freq=time_span)
    time_base_df = pd.DataFrame({'timestamp': time_index})


    # Merge FOA to time base
    FOA_merged = pd.merge_asof(
        time_base_df,
        FOA_df_filtered.sort_values('Time'),
        left_on='timestamp',
        right_on='Time',
        direction='nearest',
        tolerance=pd.Timedelta(tolerance)
    )

    # Merge Ammonit to time base
    Ammonit_merged = pd.merge_asof(
        time_base_df,
        Ammonit_df_filtered.sort_values('datetime'),
        left_on='timestamp',
        right_on='datetime',
        direction='nearest',
        tolerance=pd.Timedelta(tolerance)
    )

    # Final merged DataFrame with clean timestamps
    merged_df = pd.merge(
        FOA_merged[['timestamp', 'wind_m7']],
        Ammonit_merged[['timestamp', 'Avg wind speed', 'Max wind speed', 'Min wind speed', 'Wind angle']],
        on='timestamp'
    )

    # Derived metrics
    merged_df['abs error'] = abs(merged_df['wind_m7'] - merged_df['Avg wind speed'])
    merged_df['avg wind speed'] = 0.5*(merged_df['wind_m7'] + merged_df['Avg wind speed'])

    merged_df.rename(columns={
        'wind_m7': 'FOA wind',
        'Avg wind speed': 'Ammonit wind (avg)',
        'Max wind speed': 'Ammonit wind (max)',
        'Min wind speed': 'Ammonit wind (min)'
    }, inplace=True)


    # Interpolate missing values based on time
    merged_df.set_index('timestamp', inplace=True)
    merged_df.interpolate(method='time', inplace=True)
    merged_df.reset_index(inplace=True)

    if exclude_ranges:
        for range_start, range_end in exclude_ranges:
            start_excl = pd.to_datetime(range_start)
            end_excl = pd.to_datetime(range_end)
            merged_df = merged_df[~((merged_df['timestamp'] >= start_excl) & (merged_df['timestamp'] <= end_excl))]




    return merged_df