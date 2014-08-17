# run.md

`run.py` serves as the entry point for the program.

    $imports
    import click
    import album

## Main

We use [click](http://click.pocoo.org) for CLI interface handling. We define a group that will contain the script's commands.

    $click basics
    @click.group()
    def root():
        pass

And the main method

    $entry point
    if __name__ == '__main__':
        root()


## Build command

The primary command in the `album` compiler is **build**, which converts a specified Markdown source file to a compiler/interpreter-readable 'source' file in whatever language.

    $build method
    @root.command()
    @click.argument('src')
    @click.argument('dest')
    def build(src, dest):
        with open(src, 'r') as f:
            src_content = f.read()
    
        fp = album.FileCompiler(src_content)
    
        with open(dest, 'w') as f:
            f.write(fp.output())


# run.py

    $_main
    #!/usr/bin/env python
    %imports
    %click basics
    %build method
    %entry point
