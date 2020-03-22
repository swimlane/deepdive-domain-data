import re

import confusables

from corona  import Corona

term_list = []

master_blacklist_path = './data/blacklist/'

search_terms = []
blacklist_config = open('blacklist.config', 'r').read().split('\n')
for search_term in blacklist_config:
    if len(search_term.strip()) > 0:
        search_terms.append(search_term.strip())

for item in search_terms:  # ['corona','coronav','covid','pandemic','virus','vaccine']:
    term_list.append({
        'term': item,
        'value': re.compile(confusables.confusable_regex(item, include_character_padding=False), re.IGNORECASE | re.UNICODE)
    })
corona = Corona().generate(term_list)
