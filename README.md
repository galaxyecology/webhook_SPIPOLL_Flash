# GAPARS_Galaxy webhook

This repo is the first Galaxy webhook created thanks to the [GAPARS H2020 project](http://gapars.mmos.ch/) allowing to create connection between the MMOS (Massively Multi Online Science) portal and [SPIPOLL project](https://www.spipoll.org/) so Galaxy can display a fly picture that the user can classify, here, for SPIPOLL Flash protocol, task is to try recognizing male or female hoverflies.

A big thank to Helena Rasche particularly but Freiburg Galaxy team and Galaxy community who allow this to become reality!

## Requirements

```
pip install -r requirements.txt
```

## Obtaining a Task

```
python mmos.py
```

I receive this stdout:

```
{'description': 'Massively Multiplayer Online Science - Citizen Science Server '
                'API 2, © 2015-2017 MMOS Sàrl',
 'homepage': 'http://mmos.ch',
 'name': 'mmos-api-2',
 'stats': {'architecture': 'x64',
           'nodeEnv': 'depo',
           'nodeVersion': 'v10.16.0',
           'platform': 'linux',
           'uptime': 863153.721,
           'uptimeFriendly': '10 days',
           'uptimeSince': '2019-08-23T11:57:48.550Z'},
 'version': '2.7.42'}

{ statusCode: 201,
  body:
   { uid: '81e5fe2a-d6cc-45ca-8bf0-688dea7b0c47-1559059164041',
     game: 'yvan-le-bras-mnhn-fr',
     player: { code: 'YVAN001', accountCode: 'YVAN001' },
     task:
      { id: 10000101,
        run: 1,
        project: 'spipoll-fly',
        isTrainingSet: true,
        difficulty: 1,
        assets: [Object] } } }
{ url:
   'https://assets.mmos.io/spipoll-fly/tasks/20190503110753/1473621845158.jpg?Expires=1559059344&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9hc3NldHMubW1vcy5pby9zcGlwb2xsLWZseS90YXNrcy8yMDE5MDUwMzExMDc1My8xNDczNjIxODQ1MTU4LmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU1OTA1OTM0NH19fV19&Signature=oaxkaZXmhFOpvBMBmndaz3yvIPKKrYAt2aG~TCgAM--bhZltR87Wm6MNYiKEVslCAvOcAqyUadmlOUmVswAfyKqsgsheSsN9MxWKLk4S7UvaruWBfz0fe9TSTSCJ1cxDeN7yU-FeWCbWNbb5PRXCme7~TTUWASM55Ek1Wp~RXUoQ8WESPEQuC~WipmnVKjKl9cmAe0EMlnEQ7HckTlacBvB1gzM-pDC8wf~hkKIsf~boOcMauwoZl8UvrWjfSwmPKF-xdipWuy9Le-e6ooy8o~lIWuESbozwrov9NQbZRADvyXvH-~LXMWKG9mwPZOrdUEfMh5I-VgXzHhYcY87U~g__&Key-Pair-Id=APKAJER6OUQU7K7FS64A' }
```

Where the URL allows to download the picture and display it

![result](MMOS_Galaxy_bee.png)

So idea is to use this on 2 different manners:

- first, to display a randomizely selected picture of fly once a galaxy user submitted a job using webhook functionality in the same spirit than you made with PhDcomics
- second, to import a picture into a Galaxy history, so the user can use bioimaging tools inside Galaxy to treat / analyse the picture and send the results back to MMOS. Here we will use a "classical Galaxy tool" to get picture and another one to send analysis results


The next step will be to make similar work to allow the Galaxy user to send its task answer to MMOS through the MMOS API api.classifications.create function. Here we are working on the index.js.classification file

This assumes you have saved the create task timestamp in task.created, and that the result variable corresponds to it's validation schema (attached), essentially, your result variable should be one of the following: ["female", "likelyFemale", "cantSee", "likelyMale", "male"]
Please note it's case sensitive.


So the idea is :
- using the "task:create" function (through index.js), Galaxy can display a bee picture
- the user has to clic on one of the answer possibilities ("female", "likelyFemale", "cantSee", "likelyMale", "male"), the selected answer is stored in task.created.
- the "classification" funtion is "called" (through index.js.classification) and give the answer, for example "female", to MMOS portal.
