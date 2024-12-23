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
intel_csv_cols = set.intersection(*[set(df.columns) for df in intel_csvs])
intel_csv = pl.concat((df.select(pl.col(c) for c in intel_csv_cols) for df in intel_csvs), how="vertical")

# But then I found these, these seem to only exist for some sets of client
# parts, they aren't part of a generic database but seem more like something PMs
# are manually compiling.
# https://www.intel.com/content/www/us/en/support/articles/000005505/processors.html
# https://www.intel.com/content/www/us/en/support/articles/000028083/processors.html
INTEL_XLSX_PATHS = {
    "desktop": "assets/intel_xlsx/desktop.xlsx",
    "laptop": "assets/intel_xlsx/laptop.xlsx",
}

def parse_intel_xlsx(path):
    # There is noise in the first few rows but the parser seems clever enough to ignore it.
    # But there is one row of noise we have to slice off manually.
    df = pl.read_excel(path).slice(1)
    # Then turn the next row into column headers.
    return df.rename(df.head(1).to_dicts().pop())
intel_xlsxs = {k: parse_intel_xlsx(p) for k, p in INTEL_XLSX_PATHS.items()}
# They also have different columns. Some of them are just different names for
# the same thing so squash those here.
intel_xlsxs["desktop"] = intel_xlsxs["desktop"].rename({
    "Intel® Core™ \r\nGen": "Intel® Core™ Generation",
    "# of Cores": "# cores ",
    "# of P-cores": "# of Performance-cores",
    "# of E-cores": "# of Efficient-cores",
    "# of Threads": "# Threads",
    "Processor Base Power (previously Thermal Design Power (TDP)) \r\n(W)": "Processor Base Power (previously known as TDP)",
    
})
# There's no "Low-powere efficient cores" column in the desktop sheet, fil it in with 0s.
intel_xlsxs["desktop"] = intel_xlsxs["desktop"].with_columns(pl.lit("0").alias("# of Low Power Efficient-cores"))

print(intel_xlsxs["desktop"].columns)
print(intel_xlsxs["laptop"].columns)
intel_xlsx_cols = set.intersection(*[set(df.columns) for df in intel_xlsxs.values()]) 
print(intel_xlsx_cols)
intel_xlsx = pl.concat((df.select(pl.col(c) for c in intel_xlsx_cols) for df in intel_xlsxs.values()), how="vertical")
print(intel_xlsx)