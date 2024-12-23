import polars as pl

# Got these by clicking around in
# https://www.intel.com/content/www/us/en/ark.html.
# Their website doesn't actually seem designed to offer this info, its
# "product comparison" page lets you compare between different product
# lines, and you can in theory compare arbitrarily many SKUs with enough
# clicking around but when you try to actually generate the comparison
# it easily times out if there are more than about 100.
# So I've done that for a bunch of them but there are still way more
# Intel CPUs that haven't been done.
INTEL_CSV_PATHS = [f"assets/intel_csv/{f}" for f in [
    "Core_Gen10.csv",
    "Core_Gen11.csv",
    "Core_Gen12.csv",
    "Core_Gen13.csv",
    "Core_Gen14.csv",
    "Core_Gen8.csv",
    "Core_Gen9.csv",
    "Core_N.csv",
    "Core_Series1.csv",
    "Core_Ultra.csv",
    "Core_Ultra_Series2.csv",
    "Core_X.csv",
]]

# First two rows of the CSV are noise, ignore that.
# Spreadsheet is sideways so transpose it to make one CPU per row.
# We can't use the lazy API here as you can't transpose that.
intel_csvs = [pl.read_csv(p, skip_rows=2).transpose() for p in INTEL_CSV_PATHS]
# The CSV you get from the website has different fields depending on which products you're comparing.
# So just figure out the intersection so we can join into a single DataFrame.
intel_cols = set.intersection(*[set(df.columns) for df in intel_csvs])
intel_csv = pl.concat((df.select(pl.col(c) for c in intel_cols) for df in intel_csvs), how="vertical")

# But then I found these, these seem to only exist for some sets of client
# parts, they aren't part of a generic database but seem more like something PMs
# are manually compiling.
# https://www.intel.com/content/www/us/en/support/articles/000005505/processors.html
# https://www.intel.com/content/www/us/en/support/articles/000028083/processors.html
INTEL_XLSX_FILES = [f"assets/intel_xlsx/{f}" for f in ["server.xlsx", "laptop.xlsx"]]