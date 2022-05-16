# This script loads results from a bunch of hypertuning assimilation directories
# and displays the (sorted) results. 
# It is a python script instead of a notebook so that you can "watch" it as your
# experiments run: `watch -n 20 python hypertuning_analysis`
# 
# Sorry that the columns aren't named in the output, but this is mostly a tool
# for monitoring during rutime. You can figure it out. 

# Imports
import glob
import numpy as np
import pandas as pd
import pathlib
import os

# Change these directories to match yours. They have timestamps that depend on when the run was created.
base_assim_file = 'runs/pub/assimilation/assimilation_kfold_0_seed_0_holdout_0.5_lead_1/test/model_epoch030/test_metrics.csv'
base_ar_file = 'runs/pub/autoregression/pub_autoregression_holdout_0.5_kfold_0_seed_0_2104_214048/test/model_epoch030/test_metrics.csv'
base_sim_file = 'runs/pub/simulation/pub_simulation_kfold_0_seed_0_1304_022120/test/model_epoch030/test_metrics.csv'
hyper_dir = 'runs/pub/hyper_tuning'

base_assim = pd.read_csv(base_assim_file)
base_ar = pd.read_csv(base_ar_file)
base_sim = pd.read_csv(base_sim_file)

print(f'Simulation: {base_sim["NSE"].median()}')
print(f'Autoregression: {base_ar["NSE"].median()}')
print(f'Default Assimilation: {base_assim["NSE"].median()}')

assimilation_windows = [1, 3, 5, 10, 20]
epochs = [5, 10, 100, 1000]
histories = [1, 5, 10, 20]
learning_rates = [1e-5, 1e-4, 1e-3, 1e-2]
learning_rate_drop_factors = [0.5]
asssimilation_targets_lists = [0]

hyper_index = pd.MultiIndex.from_product([
    assimilation_windows, 
    epochs,
    histories,
    learning_rates,
    learning_rate_drop_factors,
    asssimilation_targets_lists,
    ]
)
hyper_results = pd.DataFrame(index=base_sim.index, columns=hyper_index)

hyper_files = glob.glob(str(pathlib.Path(hyper_dir) / '**' / 'test' / 'model_epoch030' / 'test_metrics.csv'))

for f in hyper_files:
    if os.path.exists('/'.join(f.split('/')[0:-1]) + '/test_results_data_assimilation.p'):
        window = int(f.split('window_')[-1].split('_')[0])   
        epoch = int(f.split('epoch_')[-1].split('_')[0])   
        history = int(f.split('history_')[-1].split('_')[0])   
        rate = float(f.split('rate_')[-1].split('_')[0])   
        drop = float(f.split('drop_')[-1].split('_')[0])
        target = int(f.split('targets_')[-1].split('/')[0])      
        results = pd.read_csv(f)
        hyper_results[(window, epoch, history, rate, drop, target)] = results['NSE']

print(hyper_results.median().dropna().sort_values())

n_complete = hyper_results.median().dropna().sort_values().shape[0]
print(f'A total of {n_complete} runs are complete.')