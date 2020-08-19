from utils_s3 import get_etf_holdings, list_keys

# list available files in s3 bucket
etf_files = list_keys(Bucket='ishares')

# get a single file from s3
df_small = get_etf_holdings('IWV', '2020-07-31')

