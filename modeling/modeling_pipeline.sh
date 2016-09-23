# Update featurization? 
# Run this shell script to retrain the models

# rm ./results/*
rm -r ./results/
mkdir results
mkdir results/final_models
python ../conversion_scripts/convert_pilotly_data.py ../data/pilotly_data/VersaillesAllData_OpenEndsAndSentiment09222016.csv
python 1_featurize_training_dat.py
python 2_grid_search_CV.py

