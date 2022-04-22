import os
import csv
import sys
import json
import click
import nothoney

stdin = None
if not sys.stdin.isatty():
    stdin = sys.stdin.read().rstrip()

defang_str = lambda s: s.replace('.', '[.]').replace('http', 'hxxp')
refang_str = lambda s: s.replace('[.]', '.').replace('hxxp', 'http')

@click.command()
@click.option('-c',  '--csv_in',     required=False)
@click.option('-cp', '--copy',       is_flag=True)
@click.option('-d',  '--delimiter',  default='\n')
@click.option('-df', '--defang',     is_flag=True)
@click.option('-j',  '--json_in',    required=False)
@click.option('-jl', '--json_lines', required=False)
@click.option('-n',  '--newlines',   is_flag=True)
@click.option('-o',  '--output',     required=False)
@click.option('-r',  '--reverse',    is_flag=True)
@click.option('-rf', '--refang',     is_flag=True)
@click.option('-s',  '--sort',       is_flag=True)
@click.option('-sp', '--splunk',     is_flag=True)
@click.option('-t',  '--terms',      is_flag=True)
@click.option('-u',  '--uniq',       is_flag=True)
def main(
    csv_in,
    copy,
    delimiter,
    defang,
    json_in,
    json_lines,
    newlines,
    output,
    reverse,
    refang,
    sort,
    splunk,
    terms,
    uniq,
):
    if not stdin:
        return

    data = stdin.split(delimiter)

    if csv_in:
        data = [row[csv_in] for row in csv.DictReader(data)]
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

    if newlines:
        output = '\n'
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

    if defang:
        if type(data) == str:
            data = defang_str(data)
        elif type(data) == list:
            data = [defang_str(i) for i in data]
    if refang:
        if type(data) == str:
            data = refang_str(data)
        elif type(data) == list:
            data = [refang_str(i) for i in data]

    print(data)

if __name__ == '__main__':
    main()
