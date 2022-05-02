import os
import ast
import csv
import sys
import json
import click
import nothoney
import ipaddress

__version__ = '0.1.3'

stdin = None
if not sys.stdin.isatty():
    stdin = sys.stdin.read().rstrip()

defang_str = lambda s: s.replace('.', '[.]').replace('http', 'hxxp')
refang_str = lambda s: s.replace('[.]', '.').replace('hxxp', 'http')

@click.command()
@click.option('-c', '--csv_in',    required=False)
@click.option('-d', '--delimiter', required=False)
@click.option('-j', '--json_in',   required=False)
@click.option('-l', '--json_log',  required=False)
@click.option('-n', '--newlines',  is_flag=True)
@click.option('-o', '--output',    required=False)
@click.option('-p', '--python',    is_flag=True)
@click.option('-r', '--reverse',   is_flag=True)
@click.option('-s', '--sort',      is_flag=True)
@click.option('-u', '--uniq',      is_flag=True)
@click.option('-v', '--version',   is_flag=True)
@click.option(      '--add',       required=False)
@click.option(      '--addl',      required=False)
@click.option(      '--addr',      required=False)
@click.option(      '--copy',      is_flag=True)
@click.option(      '--defang',    is_flag=True)
@click.option(      '--refang',    is_flag=True)
@click.option(      '--rm',        required=False)
@click.option(      '--rml',       required=False)
@click.option(      '--rmr',       required=False)
@click.option(      '--sips',      is_flag=True)
@click.option(      '--splunk',    is_flag=True)
@click.option(      '--term',      is_flag=True)
def main(
    csv_in,
    delimiter,
    json_in,
    json_log,
    newlines,
    output,
    python,
    reverse,
    sort,
    uniq,
    version,
    add,
    addl,
    addr,
    copy,
    defang,
    refang,
    rm,
    rml,
    rmr,
    sips,
    splunk,
    term,
):
    if version or not stdin:
        print(f'v{__version__}, https://github.com/vesche/bombchu')
        return
    if len([i for i in [csv_in, delimiter, json_in, json_log, python] if i]) > 1:
        print('Error! Only one of the following can be specified: -c -d -j -l -p')
        return
    if len([i for i in [output, splunk, term] if i]) > 1:
        print('Error! Only one of the following can be specified: -o --splunk --term')
        return
    if newlines:
        output = '\n'

    if csv_in:
        data = [','.join(map(str, [row[i] for i in csv_in.split(',')])) for row in csv.DictReader(stdin.splitlines())]
    elif json_in:
        data = nothoney.eat(json.loads(stdin), json_in)
    elif json_log:
        data = [','.join(map(str, [json.loads(log)[i] for i in json_log.split(',')])) for log in stdin.splitlines()]
    elif python:
        data = ast.literal_eval(stdin)
    else:
        data = stdin.split(delimiter or '\n')

    if uniq:
        data = list(set(data))
    if sort:
        data = sorted(data)
    if sips:
        data = list(map(str, sorted(ipaddress.ip_address(i) for i in data)))
    if reverse:
        data = data[::-1]
    if rm:
        data = [i.removeprefix(rm).removesuffix(rm) for i in data]
    if rml:
        data = [i.removeprefix(rml) for i in data]
    if rmr:
        data = [i.removesuffix(rmr) for i in data]
    if add:
        data = [f'{add}{i}{add}' for i in data]
    if addl:
        data = [f'{addl}{i}' for i in data]
    if addr:
        data = [f'{i}{addr}' for i in data]
    if defang:
        data = [defang_str(i) for i in data]
    if refang:
        data = [refang_str(i) for i in data]

    if output:
        data = output.join(list(map(str, data)))
    elif splunk:
        data = '(' + json.dumps(data)[1:-1] + ')'
    elif term:
        data = '(' + ' OR '.join([f'TERM({i})' for i in data]) + ')'

    if copy:
        data_copy = data[:]
        if type(data) == str:
            data_copy = data_copy.replace('"', '\\\"')
        os.system(f'echo "{data_copy}" | tr -d "\\n" | pbcopy')

    print(data)

if __name__ == '__main__':
    main()
