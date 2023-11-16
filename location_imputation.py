import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from haversine import haversine

class nearest_location_imputation:
    
    def __init__(self, df, lat_col, lon_col, merge_cols=None):


        '''Class takes the following parameters:
          df: dataframe that requires missing values imputing.
          lon_col: column within df that contains longitude
          merge_cols: additional merging columns that may be required in order to accurately merge imputed data (optional).
        ''' 
      
        if merge_cols != None:
            merge_cols.extend([lat_col, lon_col]) 
            self.merge_cols = merge_cols

        else:
            self.merge_cols = [lat_col, lon_col] 
            
        self.cols = [col for col in df.columns if col not in self.merge_cols]
        self.df_closest = self.precompute_nearest_indices(df, lat_col, lon_col)
        self.imputed = self.impute_missing_values_all_columns(lat_col, lon_col)
        
    # Precompute nearest indices for each unique week and year
    def precompute_nearest_indices(self, df, lat_col, lon_col):

        unique_lat_lon = df.loc[:, [lat_col, lon_col]].drop_duplicates(subset=[lat_col, lon_col])
        unique_lat_lon.reset_index(inplace=True, drop=True)
        dists = cdist(unique_lat_lon, unique_lat_lon, haversine)

        # Create a boolean mask for non-zero distances
        distance_mask = (dists != 0)  

        min_indices = np.argmin(np.where(distance_mask, dists, np.inf), axis=1)

        unique_lat_lon['Closest Index'] = min_indices
        merged = pd.merge(unique_lat_lon.set_index('Closest Index'), unique_lat_lon.rename(columns={lat_col:'closest_lat', lon_col:'closest_lon'}),how='left',left_index=True,right_index=True)
        return pd.merge(df, merged.drop(columns='Closest Index'),how='left', on=[lat_col, lon_col])

    # Generalized function to impute missing values for all columns
    def impute_missing_values_all_columns(self,lat_col, lon_col):
        
        col_renames = {col: col + '_closest' for col in self.cols}
        merged = pd.merge(self.df_closest, self.df_closest.rename(columns=col_renames), how='left', left_on = ['closest_lat', 'closest_lon'],right_on = [lat_col, lon_col], suffixes=('', '_toDrop'))
        for col in self.cols:
            filler_col = col + '_closest'

            # Check if missings exist for relevant column
            if merged.loc[:, col].isnull().sum() > 0:
                
                merged.loc[:,col].fillna(merged.loc[:,filler_col],inplace=True)
            merged.drop(columns=filler_col,inplace=True)
            
        # tidy up dataset
        merged.rename({lat_col + '_x':lat_col, lon_col + '_x':lon_col}, inplace=True)
        merged.drop(columns=[col for col in merged.columns if '_toDrop' in col], inplace=True)
        merged.drop(columns=['closest_lat', 'closest_lon'])
        return merged
