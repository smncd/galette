from os import getenv
from argparse import ArgumentParser
from uvicorn import run as uvicorn
from galette.utils import dir_exists, setenv


def main():
    parser = ArgumentParser(
        prog='galette',
        description="Markdown-to-HTML server, built with Starlette and Uvicorn",
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )

    parser.add_argument(
        '--host', '-H',
        type=str,
        default='localhost',
        help='The host Galette should run on (default http://localhost)'
    )

    parser.add_argument(
        '--port', '-P',
        type=int,
        default=5000,
        help='The port Galette should run on (default 5000)'
    )

    parser.add_argument(
        '--export', '-e',
        type=str,
        nargs='?',
        const=True,
        default=False,
        help='Export the site as static HTML, CSS and JS.'
    )

    parser.add_argument(
        '--pages-dir', '-p',
        type=str,
        help='Path to the pages directory.'
    )

    parser.add_argument(
        '--assets-dir', '-a',
        type=str,
        help='Path to the assets directory.'
    )

    parser.add_argument(
        '--static-dir', '-s',
        type=str,
        help='Path to the static directory.'
    )

    parser.add_argument(
        '--templates-dir', '-t',
        type=str,
        help='Path to the templates directory.'
    )


    args = parser.parse_args()

    if args.debug:
        setenv('DEBUG', 'true')
    
    if isinstance(args.pages_dir, str):
        assert dir_exists(args.pages_dir)
        setenv('GALETTE_PAGES_DIR', args.pages_dir)
    
    if isinstance(args.assets_dir, str):
        assert dir_exists(args.assets_dir)
        setenv('GALETTE_ASSETS_DIR', args.assets_dir)
    
    if isinstance(args.static_dir, str):
        assert dir_exists(args.static_dir)
        setenv('GALETTE_STATIC_DIR', args.static_dir)
    
    if isinstance(args.templates_dir, str):
        assert dir_exists(args.templates_dir)
        setenv('GALETTE_TEMPLATES_DIR', args.templates_dir)
    

    if args.export:
        from galette.generator import export

        # TODO: The args.export directory is being ignored right now.
        export()
    else:
        from galette.app import app

        uvicorn(
            app=app if not getenv('RELOAD') else 'galette.app:app',
            host=args.host,
            port=args.port,
            reload=getenv('RELOAD')
        )


if __name__ == '__main__':
    main()  
