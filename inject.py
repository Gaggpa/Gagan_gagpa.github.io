import codecs
with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

with codecs.open('galleries_snippet.html', 'r', 'utf-8') as f:
    snippet = f.read()

html = html.replace('<div id="spa-galleries-container"></div>', f'<div id="spa-galleries-container">\n{snippet}\n</div>')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(html)
