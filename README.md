# ASN Canada

[Explore Canadian ASNs](https://coolcode.ca/asn-canada/)

Search by name or ASN, filter RIPEstat’s routing flag, choose an address family, and compare prefix length distributions. The complete filtered selection can be downloaded as CSV. Copy the page URL to share the selected network and filters.

<!-- coolcode:guide -->
Try AS852. The November 19, 2026 RIS tables show 683 IPv4 prefixes and 30 IPv6 prefixes for TELUS after the ten-peer threshold. Switch address family to inspect its advertised prefix lengths or open the RIPEstat source.
<!-- /coolcode:guide -->

The registry selection uses [RIPEstat’s country-ASN report](https://stat.ripe.net/data/country-asns/data.json?resource=ca&lod=1). In the November 17 edition, 2,529 ASNs were registered to Canada and 1,650 were marked routed. The country identifies a registration and gives no physical router location. Labels come from the [RIPE ASN name file](https://ftp.ripe.net/ripe/asnames/asn.txt). A missing name leaves the registry number searchable.

The IPv4 and IPv6 breakdowns count each exact prefix whose single-number origin matches the ASN and which at least ten [RIPE RIS peers](https://ris.ripe.net/docs/ris-whois/) observed in their combined tables. Default routes and AS-set origins are excluded. These are observed prefix counts. Address space utilization, customer counts and network ownership require different records. Country routing and prefix clocks can differ. The interface displays the date attached to each source.

The weekly GitHub Action refreshes and validates the edition before replacing it. Run `python scripts/refresh.py` to update it, `node --test tests/*.test.mjs` and `python -m unittest discover -s tests` to check it, and `python scripts/build.py` to produce an offline-buildable Pages site.
