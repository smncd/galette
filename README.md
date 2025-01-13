![Galette](./docs/banner.jpg)
=============================

Galette is a Markdown-to-HTML server, built with Starlette and Unvicorn.

Why does Galette exist? Mostly for fun, and because I'll maybe need it at some point. Guess we'll find out.

Getting started
---------------

The easiest way to get going is with Docker. You'll need Docker Compose installed.

Create a `compose.yaml` file like so:
```yaml
services:
  galette:
    image: registry.gitlab.com/smncd/galette
    ports:
      - 5000:5000
    volumes:
      - /path/to/your/pages/:/pages
      - /path/to/your/assets/:/assets
```

At the path specified in your `compose.yaml` file, create `index.md` (or any other page name, but make sure the name is url friendly):
```markdown
<!-- /path/to/your/pages/index.md -->

# Hello world

Galettes are very tasty!
```

You can then start the service:
```bash
docker compose up -d
```

Visit `http://localhost:5000` and you will see your markdown, rendered as HTML.

Templates and static files
--------------------------

Galette ships with some default templates, using [VanillaHtml](https://github.com/fandeytech/VanillaHTML), but you will probably want to customize it even further.

To use custom templates and/or static files, edit your `compose.yaml` from above:

```yaml
services:
  galette:
    image: registry.gitlab.com/smncd/galette
    ports:
      - 5000:5000
    volumes:
      - /path/to/your/pages/:/pages
      - /path/to/your/assets/:/assets
      - /path/to/your/templates/:/templates # <--- templates folder
      - /path/to/your/static/:/static # <--- static folder
```

The static folder can be used however you want/need, but the templates folder needs at least two files for Galette to be happy:

* `page.jinja2`: Your page template. For now, different templates aren't really supported.
* `404.jinja2`: The 404 page template.

### Tip!

Templates can have several file extensions. Galette will look for them in the following order:

1. `{name}.html.jinja2`
2. `{name}.html.jinja`
3. `{name}.jinja2`
4. `{name}.jinja`
5. `{name}.html`

As you can tell by the file extensions, Galette uses [Jinja2](https://jinja.palletsprojects.com/en/stable/templates/) for templates.

The frontmatter from your markdown files will be accessible in the templates, along with `html`, which is the body content. 

An example template could end up looking like:
```html
<!-- /path/to/your/templates/page.jinja2 -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
    </header>
    <main>{{ html }}</main>
</body>
</html>
```

If we give it this markdown:
```markdown
---
# /path/to/your/pages/pastry.md
title: Flaky pastry
---

We love that stuff!
```

You'd end up with the following rendered page:
```html
<!-- http://localhost:5000/pastry -->
<!DOCTYPE html>:
<html>
<head>
    <title>Flaky pastry</title>
</head>
<body>
    <header>
        <h1>Flaky pastry</h1>
    </header>
    <main><p>We love that stuff!</p></main>
</body>
</html>
```

Static files have the base `/static`, so `/path/to/your/static/main.css` would end up being `http://localhost:5000/static/main.css`.

A complete example is available [here](./example/)

License and Ownership
---------------------
Copyright © 2025 Simon Lagerlöf [contact@smn.codes](mailto:contact@smn.codes)   

This project is licensed under the BSD-3-Clause license - see the [LICENSE](./LICENSE) file for details.

Galette's default templates uses [VanillaHTML by Bijan Fandey](https://github.com/fandeytech/VanillaHTML), licensed under the MIT license.
