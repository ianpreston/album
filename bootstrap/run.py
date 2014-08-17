#!/usr/bin/env python
import click
import album


@click.group()
def root():
    pass


@root.command()
@click.argument('src')
@click.argument('dest')
def build(src, dest):
    with open(src, 'r') as f:
        src_content = f.read()

    fp = album.FileCompiler(src_content)

    with open(dest, 'w') as f:
        f.write(fp.output())


if __name__ == '__main__':
    root()
