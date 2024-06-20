#!/usr/bin/env python3

import pandas as pd
from pandas_profiling import ProfileReport
import webbrowser

# Kestrel analytics default paths
INPUT_DATA_PATH = "/data/input/0.parquet.gz"
OUTPUT_DISP_PATH = "/data/display/profile.html"

class PlotFailure(Exception):
    pass

def pandas_profile(df):
    prof = ProfileReport(df)
    prof.to_file(output_file=OUTPUT_DISP_PATH)
    profile_path = 'file:/'+OUTPUT_DISP_PATH
    webbrowser.open_new_tab(profile_path)


if __name__ == "__main__":
    dfi = pd.read_parquet(INPUT_DATA_PATH)
    if dfi.size == 0:
        print("The Dataframe is empty!")
    else:
        fig = pandas_profile(dfi)
