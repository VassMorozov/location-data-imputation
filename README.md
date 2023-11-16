# location_data_imputation
Considering a Pandas dataframe with latitude and longitude columns,  this class imputes missing data based on nearest location using the haversine distance. All columns for the dataframe are considered, however only ones where a missing value is present are imputed. 

The example below illustrates how this is performed. The graphic contains grey data points which contain missing values for the 'Price' column. The value is filled with those of the location closest. 
![image](https://github.com/VassMorozov/location_data_imputation/assets/28609388/6cb303a4-d05a-47a5-8b24-a0e2e929d0e8)

The dataframe may have duplicate rows for a location (for example based on year) so any additional merging columns can be passed to the class so that imputation for the location is relevant to the specific row.
