from lector import readYal
from afdd import regex_to_afd
from jinja2 import Template
import pickle

filename = './tests/slr-1.yal'
rule_token, token_dic = readYal(filename)
with open('template.j2', 'r') as f:
    template = f.read()

template = Template(template)
rendered = template.render(tokens=token_dic)
with open('scanner.py', 'w') as f:
    f.write(rendered)

afdd = regex_to_afd(rule_token, token_dic)
print("scanner.py generado correctamente")
with open('afdd.pickle', 'wb') as f:
    pickle.dump(afdd, f)
