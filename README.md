# Corona Domain Data

> This project contains curated data related to coronavirus pandemic and will continue housing historical data associated with registered most domains

This repository contains data related to coronavirus & COVID-19 based domains identified by Swimlane's DeepDive research team.  We are providing three generated files to assist researchers, security, and IT teams with combatting phishing and other malicious attacks associated with identified domains.

## Provided JSON Files

Our team has and will continue to generate daily JSON files which can be used for further research and defensive measures.  These JSON files are named based on the term used during generation.  The following terms are used and a generated JSON file is created with each of these terms pre-pended to the appropriate type of file:

* corona
* coronav
* covid
* pandemic
* virus
* vaccine

The file formats you will find, each day, are located with in the [Data](data) folder in this repository and will be contained under their appropriate date:

* {term}_ip.json
    * The datasets ending in `_ip.json` takes all the identified domains and retrieves their A record IP address.  With this JSON file you are able to see which domains are associated with a specific IP address.
* {term}_zone.json
    * The datasets ending in `_zone.json` creates a list of dictionaries for each TLD.  Each of these dictionaries contains the actual identified domain and the ip address for this domain based on their A record IP address. 
* master_blacklist.txt
    * This file contains a blacklist of all terms and their identified domains, except for domains ending in .gov.  More than likely you should blacklist all of these domains but use at your own discretion.

## Identification of Domains

By utilizing CZDS (Centralized Zone Data Service) we are examining all domains for approximately 900 gTLDs. We are examining each domain for both a string match as well as IDN or confusable characters when identifying a domain which matches a term.

The result of this data, is that we are looking for domains which may be using uncommon characters, which is typically used during phishing attacks.  

Additionally, each file generated for each term has it's own structure to assist with the analysis and detection of potentially malicious domains as well IP address blocks associated with malicious domains.

## {term}_ip.json

The `{term}_ip.json` file has the following data structure (as an example only):

```json
{
   "192.64.119.149":[
      "coronanet.app",
      "coronanet.app"
   ],
   "50.63.202.50":[
      "coronanews.app",
      "coronanews.app"
   ],
   "23.23.202.83":[
      "coronanotify.app",
      "coronanotify.app"
   ],
   "151.101.65.195":[
      "coronavirus.app",
      "coronavirus.app"
   ],
   "151.101.1.195":[
      "coronavirus.app",
      "coronavirus.app"
   ]
   ....
}
```

## {term}_zone.json

The `{term}_zone.json` file has the following data structure (as an example only):

```json
{
   "app":[
      {
         "domain":"coronanearme.app",
         "ips":null
      },
      {
         "domain":"coronanearme.app",
         "ips":null
      },
      {
         "domain":"coronanet.app",
         "ips":[
            "192.64.119.149"
         ]
      },
   ],
   "mil":[
      {
         "domain":"coronanet.mil",
         "ips":[
            "192.64.119.149"
         ]
      },
      {
         "domain":"coronanews.mil",
         "ips":[
            "50.63.202.50"
         ]
      },
      {
         "domain":"coronanews.mil",
         "ips":[
            "50.63.202.50"
         ]
      }
   ]
   ....
}
```

## {term}_blacklist.json

The `{term}_blacklist.json` file has the following data structure (as an example only):

```text
coronanet.app
coronanet.app
coronanews.app
coronanews.app
coronanotify.app
coronanotify.app
coronavirus.app
coronavirus.app
coronavirus.app
coronavirus.app
....
```

## Configuration

This repository will automatically be updated on a daily basis with new data files and will hold for the forseeable future daily generated files for use be security, research, and IT teams to assist with the defense of coronavirus related attacks.

## Contributing

If you believe that a domain should be whitelisted or not included in our blacklist please submit an issue in this repository and we will resolve this as soon as possible.

Please read [CONTRIBUTING.md](https://github.com/swimlane/corona-domain-data/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Change Log

Please read [CHANGELOG.md](https://github.com/swimlane/corona-domain-data/blob/master/CHANGELOG.md) for details on features for a specific version of `corona-domain-data`

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/swimlane/corona-domain-data/blob/master/LICENSE.md) file for details

## FEEDBACK

Please submit any feedback, including defects and enhancement requests at: 

[Issues](https://github.com/swimlane/corona-domain-data/issues)

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/msadministrator)
* Nick Tausek - *Initial work* - [nikkuman](https://github.com/nikkuman)

See also the list of [contributors](https://github.com/swimlane/corona-domain-data/contributors) who participated in this project.

