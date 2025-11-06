import re

lexicon = [
    ('(?P<group1>a)(?P<group2>b)', None),  # Named capturing groups
]

scanner = re.Scanner(lexicon)
result, leftover = scanner.scan("ab")  # Segmentation fault occurs here
