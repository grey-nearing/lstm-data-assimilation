Code for paper:

Nearing et al., (2022) Technical Note: Data assimilation and autoregression for using near-real-time streamflow observations in long short-term memory networks. Hydrology and Earth Systems Science Discussions.

Once cloned, it is necessary to get the CAMELS dataset:

1) CAMELS data from NCAR:

The standard NCAR CAMELS dataset here: https://ral.ucar.edu/solutions/products/camels. 

Download and unzip the `CAMELS time series meteorology, observed flow, meta data (.zip)` file and the `CAMELS Attributes (.zip)` file. Unzip these and place the `camels_attributes_v2.0` directory in the `basin_dataset_public_v1p2` directory (this isnecessary so that NeuralHydrology can read the basin attributes).

2) Extend CAMELS forcings:

These are forcing datasets for CAMELS extended through 2014.

Maruer: https://www.hydroshare.org/resource/17c896843cf940339c3c3496d0c1c077/
NLDAS: https://www.hydroshare.org/resource/0a68bfd7ddf642a8be9041d60f40868c/

Unzip/untar these and place the resulting `*_extended` directories in 
`basin_dataset_public_v1p2/basin_mean_forcing'.


The following steps recreate the experiments for the paper.

1) Run the notebook `create_configs.ipynb`. All you have to do is change the working directory to your local path. You can modify the experiment parameters here, if you want (e.g., lead times, fractions of holdout for training, etc.).

2) Run NeuralHydrology on the config files created by that notebook. Use the `neuralhydrology/neuralhydrology/nh_run_scheduler.py` script -- e.g., to run the simulation runs use: `python neuralhydrology/nh_run_scheduler.py train --directory=run_configs --gpu-ids 0 1 2 3 --runs-per-gpu=2`.

3) Hypertuning. After the PUB simulation models are finished training, run the `create_hypertuning_directories.ipynb` notebook. This creates a hyper_tuning directory under `~/runs/pub`. Then run the hypertuning experiments with `python neuralhydrology/nh_run_scheduler.py evaluate --directory=runs/pub/hyper_tuning --gpu-ids 0 1 2 3 --runs-per-gpu=3 --data-assimilation=True`. 

You can use the results from this to set the default assimilation hypermarameters in the `create_da_asn_ar_test_directories.ipynb` notebook. They are currently set to the best hypers I found with the hyper sweep reported in the paper.

4) Evaluation. Run `create_da_asn_ar_test_directories.ipynb` to create all of the test directories with different inference settings (e.g., test holdout, lead_times, etc.). This will create many replicates of the directories containing trined models. Then run NeuralHydrology in inference mode on all of these directories: e.g., 

For DA: `python neuralhydrology/nh_run_scheduler.py evaluate --directory=runs/time_split/assimilation --gpu-ids 0 1 2 3 --runs-per-gpu=3 --data-assimilation=True`.

For AR: `python neuralhydrology/nh_run_scheduler.py evaluate --directory=runs/time_split/autoregression --gpu-ids 0 1 2 3 --runs-per-gpu=3`.

5) Once everything has completed running, use the analysis notebooks to create the figures in the paper.
