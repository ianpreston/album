# FileCompiler class

Here's the majority of the functionality. The FileCompiler class takes Markdown source and converts it to the intermediate source that is read by the compiler/interpreter (in `album`'s case, Python).

Roughly, this is the process FileCompiler implements:
* Extract code blocks from the Markdown file
* Build a map of block name : block content
* Recursively resolve block refs, starting from the _main block
* The resolved contents of the _main block become the output


## Public interface

FileCompiler's interface is just a constructor and the `output()` method, which takes no arguments and returns the compiled output for this file.


    $public interface
    def __init__(self, source):
        %constructor
    
    def output(self):
        return self.blocks['_main']

    def process_block_references(self, name):
        self.blocks[name] = self._process_block_references(
            name,
            self.blocks[name],
        )


## Extract code blocks

### Mistune

To extract code blocks from Markdown, we use the [mistune](https://github.com/lepture/mistune) Markdown parser for python.

We implement a custom renderer class called `BlockRecordRenderer`. When mistune parses the file, it will call `BlockRecordRenderer.block_code` for each code block (expecting rendered HTML for that code block). `BlockRecordRenderer` just keeps an internal list of all the code blocks it has encountered.

    $renderer class
    class BlockRecordRenderer(mistune.Renderer):
        def __init__(self, *args, **kwargs):
            super(BlockRecordRenderer, self).__init__(*args, **kwargs)
            self.blocks = []
    
        def block_code(self, code, lang):
            self.blocks.append(code)
            return ''

In the `FileCompiler` class we simply run mistune with our custom renderer, then iterate over its list of code blocks and build a `name : content` map (see below).

    $extract code blocks
    def _grab_blocks(self):
        r = BlockRecordRenderer()
        mistune.markdown(self.source, renderer=r)
    
        blocks = {}
        for block in r.blocks:
            name, content = self._parse_raw_block(block)
            blocks[name] = content        
        self.blocks = blocks

### Building a map

The first line of a block must start with a dollar sign. Every character after the `$` is part of that line's name. The rest of the lines until the end of the Markdown code block are part of the block's content. Here we define a method that splits a block into its name and content.

    $split block name and content
    def _parse_raw_block(self, raw_block):
        lines = raw_block.splitlines()
        if len(lines) < 2:
            raise LPSyntaxError('Invalid block - must not be empty')
        if not lines[0].startswith('$'):
            raise LPSyntaxError('Invalid block - must start with name')
        
        name = lines[0].strip('$').strip()
        content = '\n'.join(lines[1:]).strip()
        return name, content 

### Resolving References

Lines within a block that begin with a `%` character are references to other blocks (blockrefs). We should grab the contents of the referenced block, and inject it in place of the reference line.

This process is then continued recursively, until all blockrefs are resolved.

We begin by iterating over each line in the block, processing each line that begins with a %.

    $resolve references
    def _process_block_references(self, name, content):
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if not line.lstrip().startswith('%'):
                new_lines.append(line)
                continue

            %resolve an individual reference

        return '\n'.join(new_lines)

-

    $resolve an individual reference
    %get indent level
    %get block content
    %recurse
    %append

First, determine the indentation level of the `%`, as we will indent the entire code block line-by-line to match this indentation level. This is necessary for languages like Python, where indentation is significant.

    $get indent level
    indent = line[:line.index('%')].count(' ')

Next, parse out the name of the referenced block, and get the content of that block.

    $get block content
    ref_name = line.strip().lstrip('%')
    ref_content = self.blocks.get(ref_name)
    if not ref_content: 
        raise LPSemanticError('Invalid ref: {}'.format(ref_name))

Recursively resolve all references in that block.

    $recurse
    ref_content = self._process_block_references(ref_name, ref_content)

Finally, append the resolved contents of that block in place of the current blockref line.

    $append
    for rcl in ref_content.splitlines():
        rcl = (' ' * indent) + rcl
        new_lines.append(rcl)


## Kicking it off

We start the whole parsing process in the constructor, simply by resolving the `_main` block.

    $constructor
    self.source = source
    self.blocks = None
    self._grab_blocks()
    if not self.blocks.get('_main'):
        raise LPSemanticError('Source file must define _main block')
    self.process_block_references('_main')


# compiler.py

    $imports
    import mistune
    from errors import LPSyntaxError, LPSemanticError

-

    $FileCompiler class
    class FileCompiler(object):
        %public interface
        %extract code blocks
        %split block name and content
        %resolve references

-

    $_main
    %imports
    %FileCompiler class

    %renderer class
