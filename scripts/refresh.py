"""Build the Canadian ASN directory from RIPEstat, the RIPE ASN name list and RIS."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import gzip
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / 'web/data'
COUNTRY = 'https://stat.ripe.net/data/country-asns/data.json?resource=ca&lod=1'
NAMES = 'https://ftp.ripe.net/ripe/asnames/asn.txt'
RIS = 'https://www.ris.ripe.net/dumps/riswhoisdump.IPv{}.gz'

def fetch(url):
    return urlopen(Request(url,headers={'User-Agent':'CoolCode ASN Canada'}),timeout=120)

def member_list(value):
    if isinstance(value,list):
        return {int(x) for x in value}
    return {int(n) for n in re.findall(r'AsnSingle\((\d+)\)',value)}

def prefix_counts(family, roster):
    counts = {asn:{} for asn in roster}
    stamp = None
    lines = 0
    with fetch(RIS.format(family)) as response, gzip.GzipFile(fileobj=response) as stream:
        for raw in stream:
            line = raw.decode('ascii',errors='replace').strip()
            if line.startswith('% This file was generated at'):
                stamp = datetime.strptime(line.removeprefix('% This file was generated at ').rstrip('.'),'%a %b %d %H:%M:%S UTC %Y').date().isoformat()
            if not line or line.startswith('%'):
                continue
            asn, prefix, peers = line.split()
            if not asn.isdecimal() or int(asn) not in roster or int(peers) < 10:
                continue
            length=int(prefix.rsplit('/',1)[1])
            if length == 0:
                continue
            dist = counts[int(asn)]
            dist[length] = dist.get(length,0)+1
            lines += 1
    if not stamp or not lines:
        raise ValueError('Missing dated RIS origins')
    return stamp,counts

def main():
    with fetch(COUNTRY) as r:
        query=json.load(r)['data']
    c = query['countries'][0]
    routed = member_list(c['routed'])
    roster = routed | member_list(c['non_routed'])
    if len(roster) != c['stats']['registered'] or len(routed) != c['stats']['routed'] or len(roster) < 1000:
        raise ValueError('Country-ASN cardinalities do not reconcile')
    with fetch(NAMES) as response:
        names = {}
        for line in response:
            num,sep,rest = line.decode('utf-8',errors='replace').strip().partition(' ')
            if sep and num.isdecimal() and int(num) in roster:
                names[int(num)] = re.sub(r', [A-Z]{2}$','',rest)
    with ThreadPoolExecutor(2) as executor:
        v4,v6 = executor.map(lambda family:prefix_counts(family,roster),[4,6])
    rows=[[n,names.get(n,''),n in routed,v4[1][n],v6[1][n]] for n in sorted(roster)]
    status={'retrieved':datetime.now(timezone.utc).date().isoformat(),'registry':query['query_time'][:10],
            'v4':v4[0],'v6':v6[0],'count':len(roster),'routed':len(routed),'min_peers':10}
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,obj in [('networks',rows),('status',status)]:
        (ROOT/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n')

if __name__=='__main__':
    main()
