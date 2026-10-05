import pandas as pd
import numpy as np

def load_and_preprocess_data(production_path, process_path):
    """
    Loads, cleans, and merges production and process data into a single Training/Optimization dataset.
    """
    
    import shutil
    import os
    
    temp_prod = 'temp_prod.xlsx'
    temp_proc = 'temp_proc.xlsx'
    
    # 1. Load Data
    try:
        shutil.copy2(production_path, temp_prod)
        shutil.copy2(process_path, temp_proc)
        df_prod = pd.read_excel(temp_prod)
        df_proc = pd.read_excel(temp_proc)
        print(f"Loaded Production Data: {df_prod.shape}")
        print(f"Loaded Process Data: {df_proc.shape}")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return None
    finally:
        if os.path.exists(temp_prod):
            try: os.remove(temp_prod)
            except: pass
        if os.path.exists(temp_proc):
            try: os.remove(temp_proc)
            except: pass

    # 2. Aggregate Time-Series Process Data
    # For a batch model, we typically need summary statistics of the time-series operations
    proc_numeric = df_proc.select_dtypes(include=[np.number]).columns.tolist()
    if 'Time_Minutes' in proc_numeric:
        proc_numeric.remove('Time_Minutes')
        
    # Create aggregations for the time series
    agg_funcs = {col: ['mean', 'max', 'min', 'std'] for col in proc_numeric}
    
    # Also calculate total energy consumption (Integral of Power Kw over Time)
    # Since time steps are 1 minute, sum(Power_Consumption_kW) / 60 gives kWh roughly
    if 'Power_Consumption_kW' in df_proc.columns:
         # sum of kW * (1 hr / 60 min) = kWh
         df_proc['Energy_kWh_step'] = df_proc['Power_Consumption_kW'] / 60.0
         agg_funcs['Energy_kWh_step'] = ['sum']
         
    # Group by Batch ID
    df_proc_agg = df_proc.groupby('Batch_ID').agg(agg_funcs).reset_index()
    
    # Flatten multi-indexed columns
    df_proc_agg.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_proc_agg.columns.values]
    
    # Rename Total Energy
    if 'Energy_kWh_step_sum' in df_proc_agg.columns:
        df_proc_agg.rename(columns={'Energy_kWh_step_sum': 'Total_Energy_kWh'}, inplace=True)
    
    # Fill any NaNs created by 'std' on single-row groups
    df_proc_agg.fillna(0, inplace=True)

    # 3. Merge Datasets
    # Production data holds the 'Primary Targets' (Quality, Yield) 
    # and initial 'Configuration Parameters'
    df_merged = pd.merge(df_prod, df_proc_agg, on='Batch_ID', how='inner')
    
    # 4. Define Targets and Features explicitly for clarity down the line
    
    # Define Primary Targets (From Problem Statement: Quality/Waste, Yield, Performance)
    # Based on columns:
    # Quality related: 'Content_Uniformity', 'Dissolution_Rate', 'Disintegration_Time', 'Friability', 'Moisture_Content', 'Hardness'
    # Yield related: 'Tablet_Weight'
    # Energy Target: 'Total_Energy_kWh'
    
    targets = [
        'Content_Uniformity', 
        'Dissolution_Rate', 
        'Friability', 
        'Disintegration_Time',
        'Moisture_Content',
        'Tablet_Weight',
        'Hardness',
        'Total_Energy_kWh'
    ]
    
    # Define actionable Configuration Features (Things the operator can change)
    features_config = [
        'Granulation_Time', 
        'Binder_Amount', 
        'Drying_Temp', 
        'Drying_Time',
        'Compression_Force', 
        'Machine_Speed', 
        'Lubricant_Conc'
    ]
    
    # Validate missing columns
    missing_cols = [c for c in targets + features_config if c not in df_merged.columns]
    if missing_cols:
        print(f"Warning: Expected columns missing from merged data: {missing_cols}")

    print(f"Final Merged Dataset Shape: {df_merged.shape}")
    
    return {
        'data': df_merged,
        'features': features_config,
        'targets': targets
    }

if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prod_path = os.path.join(base_dir, '_h_batch_production_data.xlsx')
    proc_path = os.path.join(base_dir, '_h_batch_process_data.xlsx')
    
    result = load_and_preprocess_data(prod_path, proc_path)
    
    if result:
        df = result['data']
        print("\nPipeline Test Successful.")
        print(f"Identified {len(result['features'])} configurations & {len(result['targets'])} targets.")
        print("\nSample Data (First 3 rows of Targets and Features):")
        display_cols = ['Batch_ID'] + result['features'][:3] + result['targets']
        print(df[display_cols].head(3))
