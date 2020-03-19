import argparse
import re

import confusables

from corona  import Corona

def main(string_value):
    term_dict = {
        'term': string_value,
        'value': re.compile(confusables.confusable_regex(string_value, include_character_padding=False), re.IGNORECASE | re.UNICODE)
    }
    corona = Corona().generate(term_dict['term'], term_dict['value'])
    print(corona)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Generates JSON data file based on the provided string value')
    parser.add_argument('term', help='The term to generate a JSON data file for')
    args = parser.parse_args()

    main(args.term)