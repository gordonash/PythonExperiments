import re
text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha HaHa

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''
pattern=re.compile(r'(\d{3})(-|.|\*)(\d{3})')

matches=pattern.findall(text_to_search)
print (matches)
#for match in matches:
  #  print(match.group(0))

exit()
with open('data.txt','r',encoding='utf-8' )as f:
    contents=f.read()
    pattern=re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
    matches=pattern.finditer(contents)
    for match in matches:
        print(match)