# ![Galette](./docs/banner.jpg)

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


License and Ownership
---------------------
Copyright © 2025 Simon Lagerlöf [contact@smn.codes](mailto:contact@smn.codes)   

This project is licensed under the BSD-3-Clause license - see the [LICENSE](./LICENSE) file for details.

Galette uses [VanillaHTML by Bijan Fandey](https://github.com/fandeytech/VanillaHTML), licensed under the MIT license.