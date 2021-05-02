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

You can see an example output of the script to stdout in the file [`example_output.txt`](example_output.txt)

Example output of the fetched data is in json format with the timestamp as the filename, there is an example [`last-run.json`](data/last-run.json).
```----------------------------------------

2021-02-05T16:33:02 : Checking for new open slots

Clinic: Regent Park 40 Oaks
---------------------------------
Total open slots for Regent Park 40 Oaks : 0
Change since last fetch for Regent Park 40 Oaks : +0


Clinic: St. James Town Wellesley Community Centre (WCC)
---------------------------------
Group: IndigenousAdults
2021-05-03 : 1 (+0)

Total open slots for St. James Town Wellesley Community Centre (WCC) : 1
Change since last fetch for St. James Town Wellesley Community Centre (WCC) : +0


Clinic: Ryerson University
---------------------------------
Total open slots for Ryerson University : 0
Change since last fetch for Ryerson University : +0


Clinic: St. Michael’s Hospital
---------------------------------
Group: High
2021-05-04 : 7 (+0)
2021-05-05 : 9 (+0)
2021-05-06 : 7 (+0)
2021-05-07 : 7 (+0)
2021-05-08 : 5 (+0)

Group: Special
2021-05-08 : 1 (+0)

Total open slots for St. Michael’s Hospital : 36
Change since last fetch for St. Michael’s Hospital : +0


Clinic: St. Joseph’s Health Centre
---------------------------------
Group: IndigenousAdults
2021-05-03 : 1 (+0)

Group: High
2021-05-05 : 9 (+0)
2021-05-06 : 6 (+0)
2021-05-07 : 7 (+0)
2021-05-08 : 8 (+0)

Group: Special
2021-05-03 : 1 (+0)

Total open slots for St. Joseph’s Health Centre : 32
Change since last fetch for St. Joseph’s Health Centre : +0


Clinic: West Park Healthcare Centre
---------------------------------
Group: Special
2021-05-03 : 1 (+0)

Total open slots for West Park Healthcare Centre : 1
Change since last fetch for West Park Healthcare Centre : +0


Clinic: Community Hub Place
---------------------------------
Total open slots for Community Hub Place : 0
Change since last fetch for Community Hub Place : +0
```
As the script runs continuously it will be generating these json files, in future we can just rotate the fetched data into `last-run.json` file but for now it will be creating these json files for each fetch.

To stop the script just exit using a keyboard interrupt `Ctrl + c` the script will overwrite the `data/last-run.json`
