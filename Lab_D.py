from lector import readYal
from afdd import regex_to_afd
from jinja2 import Template
import pickle

archivo_yalex = './tests/slr-1.yal'
rule_token, token_dic = readYal(archivo_yalex)
with open('template.j2', 'r') as f:
    template = f.read()

template = Template(template)
rendered = template.render(tokens=token_dic)
with open('./output/scanner.py', 'w') as f:
    f.write(rendered)

afd = regex_to_afd(rule_token, token_dic)
print("AFD creado y listo")
with open('./output/afd.pickle', 'wb') as f:
    pickle.dump(afd, f)
