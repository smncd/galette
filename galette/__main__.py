from argparse import ArgumentParser
from uvicorn import run as uvicorn
from galette.app import app
from galette.generator import export

def main():
    parser = ArgumentParser(
        prog='galette',
        description="Markdown-to-HTML server, built with Starlette and Uvicorn",
    )

    task = parser.add_subparsers(dest="task", required=True)

    task_start = task.add_parser("start", help="Start Galette server")

    task_start.add_argument(
        '--host', '-H',
        type=str,
        default='localhost',
        help='The host Galette should run on (default http://localhost)'
    )

    task_start.add_argument(
        '--port', '-P',
        type=int,
        default=5000,
        help='The port Galette should run on (default 5000)'
    )

    task_export = task.add_parser("export", help="Generate static HTML.")

    args = parser.parse_args()

    if args.task == 'start':
        uvicorn(
            app=app,
            host=args.host,
            port=args.port,
        )
    elif args.task == 'export':
        export()


if __name__ == '__main__':
    main()  
