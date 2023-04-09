# python-homeautomation

## setup
Initialize requirements by doing the following
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

edit the token in the script

run the script

```sh
chmod a+x *.sh
./run.sh
```


when using docker
```
docker build -t python-homeautomation .
```

run with 
```
docker run --rm --network="host" python-homeautomation
```

install with crontab -e
```
*/5 * * * *  docker run --rm --network="host" python-homeautomation
```