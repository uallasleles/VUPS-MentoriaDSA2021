```bash
\> pip freeze > requirements.txt
```

```bash
\> pip install -r requirements.txt
```

---

Sintaxe para um caminho para um arquivo na pasta *static*:
```jinja
href="{{ url_for('static', filename='main.css') }}"
```

Sintaxe para um caminho para um arquivo dentro de uma pasta na pasta *static*:
```jinja
scr="{{ url_for('static', filename='images/foo.jpg') }}"
```

<br>

> *href* especial para arquivos na pasta "*static*" do Flask
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

---