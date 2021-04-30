# Verto Fetch Vaccine Slots

The python script here periodically fetches from the Verto API for available slots for all clinics supported by them.
The script periodically fetches every 3 minutes and displays a summary of change since the last fetch.

# Running the script

The project uses [poetry](https://python-poetry.org/docs/) for python dependency and environment management.
It is not required but highly recommended since there are multiple python versions per user's machines.

Once you have poetry installed run in the repo directory:
```shell
poetry install

#running the virtualenv defined by poetry
poetry shell

#run the python script
python get_available_slots.py

```

# Output

You see an example output of the script to stdout in the file [`example_output.txt`](example_output.txt)

Example output of the fetched data is in json format with the timestamp as the filename, there is an example [`last-run.json`](last-run.json).
As the script runs continuously it will be generating these json files, in future we can just rotate the fetched data into `last-run.json` file but for now it will be creating these json files for each fetch.

If you want to continue on from last time you left off just rename the latest run json file to `last-run.json` and run the script again.