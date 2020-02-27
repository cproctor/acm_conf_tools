# EXPECTED OUTPUT FORMAT
#"Paper Type",
#"Title",
#"Lead Author:Affiliation;Author2:Affiliation;Author3:Affiliation;etc.",
#"Lead Author e-mail",
#"Author e-mail;Author e-mail",
#"paper number"

import yaml
import csv

INFILE = "submissions.yaml"
OUTFILE = "submissions_for_acm.csv"
PAPER_TYPES = {
    "Full Papers": "Full Paper",
    "Short Papers": "Short Paper",
}

def include_paper(paper):
    return paper['track'] in PAPER_TYPES.keys() and paper['decision'] == 'Accepted'

def parse_paper(paper):
    return [
        PAPER_TYPES[paper['track']],
        paper['title'],
        ';'.join(a['first_name'] + ' ' + a['last_name'] + ':' + a['organization'] for a in paper['authors']),
        paper['authors'][0]['email'],
        ';'.join(a['email'] for a in paper['authors'][1:]),
        paper['id']
    ]

with open(INFILE) as fh:
    all_papers = yaml.safe_load(fh.read())
rows = [parse_paper(p) for p in all_papers if include_paper(p)]
with open(OUTFILE, 'w') as fh:
    writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
