from . import create_app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the benchmark result comparison webapp.')
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    app = create_app(args.debug)
    app.run()
