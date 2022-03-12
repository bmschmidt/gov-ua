This GitHub repository contains a small program to monitor Ukrainian
government websites and their availability, and log errors to the file
`data.csv`.

The list of Ukrainian government homepages was created using a [Wikidata SPARQL
query] to find URLs containing `.gov.ua`:

You can find a couple Notebooks containing some analysis in the repo:

* [Websites]: how to put the websites on a [map](https://edsu.github.io/gov-ua/Websites.html) to see where they are hosted.
* [Outage]: exploring an outage that happened on March 3 and putting them on a [map](https://edsu.github.io/gov-ua/Outage.html).

[Websites]: https://github.com/edsu/gov-ua/blob/main/Websites.ipynb
[Outage]: https://github.com/edsu/gov-ua/blob/main/Outage.ipynb
[Peter Krantz]: https://www.peterkrantz.com/
[Wikidata SPARQL query]: https://query.wikidata.org/#SELECT%20DISTINCT%20%3Furl%20WHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP856%20%3Furl%20.%0A%20%20FILTER%28CONTAINS%28LCASE%28STR%28%3Furl%29%29%2C%20%27.gov.ua%27%29%29%0A%7D
