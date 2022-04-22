import os
import csv
import sys
import json
import click
import nothoney

stdin = None
if not sys.stdin.isatty():
    stdin = sys.stdin.read().rstrip()


@click.command()
@click.option('-c',  '--csv_in',     required=False)
@click.option('-cp', '--copy',       is_flag=True)
@click.option('-d',  '--delimiter',  default='\n')
@click.option('-j',  '--json_in',    required=False)
@click.option('-jl', '--json_lines', required=False)
@click.option('-n',  '--newlines',   is_flag=True)
@click.option('-o',  '--output',     required=False)
@click.option('-r',  '--reverse',    is_flag=True)
@click.option('-s',  '--sort',       is_flag=True)
@click.option('-sp', '--splunk',     is_flag=True)
@click.option('-t',  '--terms',      is_flag=True)
@click.option('-u',  '--uniq',       is_flag=True)
def main(
    csv_in,
    copy,
    delimiter,
    json_in,
    json_lines,
    newlines,
    output,
    reverse,
    sort,
    splunk,
    terms,
    uniq,
):
    if not stdin:
        return

    if newlines:
        output = '\n'

    data = stdin.split(delimiter)

    if csv_in:
        reader = csv.DictReader(data)
        data = [row[csv_in] for row in reader]

    if json_in:
        data = nothoney.eat(json.loads('\n'.join(data)), json_in)

    if json_lines:
        data = [json.loads(i)[json_lines] for i in data]

    if uniq:
        data = list(set(data))

    if sort:
        data = sorted(data)

    if reverse:
        data = data[::-1]

    if output:
        data = output.join(list(map(str, data)))
    elif splunk:
        data = '(' + json.dumps(data)[1:-1] + ')'
    elif terms:
        data = '(' + ' OR '.join([f'TERM({i})' for i in data]) + ')'

    if copy:
        data_copy = data[:]
        if type(data) == str:
            data_copy = data_copy.replace('"', '\\\"')
        os.system(f'echo "{data_copy}" | tr -d "\\n" | pbcopy')

    print(data)


if __name__ == '__main__':
    main()
