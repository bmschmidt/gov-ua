git pull
gzip --force --keep data.csv 
git commit -m 'latest data' data.csv.gz
git push
