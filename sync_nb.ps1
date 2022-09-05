
$src = "s3://aws-emr-resources-307112368050-us-east-2/notebooks/e-B1Q0KUEQQPVFAA751EVPPQOBR/big_data_demo/"
$targ = "C:/Users/HERZOMJ/OneDrive - AbbVie Inc (O365)/Documents/GitHub/big_data_demo"
$exclude = "*.ipynb_checkpoints/**"
#aws s3 cp $src $targ --exclude "*" --include "*.ipynb" --exclude "*/*" --recursive --profile personal 
aws s3 sync $src $targ --exclude "*" --include "*.ipynb" --exclude $exclude --delete --profile personal --dryrun
pause
aws s3 sync $src $targ --exclude "*" --include "*.ipynb" --exclude $exclude --delete --profile personal 
