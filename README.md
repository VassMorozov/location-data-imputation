# location_data_imputation
Considering a Pandas dataframe with latitude and longitude columns,  this class imputes missing data based on nearest location. All columns for the dataframe are considered, however only ones where a missing value is present are imputed. 

The dataframe may have duplicate rows for a location (for example based on year) so any additional merging columns can be passed to the class so that imputation for the location is relevant to the specific row.
