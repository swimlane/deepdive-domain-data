import re

import confusables

from corona  import Corona

term_list = []

for item in ['corona','coronav','covid','pandemic','virus','vaccine']:
    term_list.append({
        'term': item,
        'value': re.compile(confusables.confusable_regex(item, include_character_padding=False), re.IGNORECASE | re.UNICODE)
    })
corona = Corona().generate(term_list)
