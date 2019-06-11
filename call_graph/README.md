# Pyan AST & Digraph




```
pip install git+https://github.com/ttylec/pyan
alias pygraph='find . -iname "*.py" | xargs pyan --dot --colored --no-defines --grouped | dot -Tpng -Granksep=1.5 | open -f -a /Applications/Preview.app'
```

pip install git+https://github.com/ttylec/pyan
cat file.py | pyan --dot --colored --no-defines --grouped | dot -Tpng -Granksep=1.5 > file.py