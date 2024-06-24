import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--browser',
                    choices=['chrome', 'undetected', 'remote'],
                    default='chrome',
                    help='browser to use')

parser.add_argument('--headless',
                    choices=['true', 'false'],
                    default='false',
                    help='headless mode')

args = parser.parse_args()
