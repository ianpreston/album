import mistune
from errors import LPSyntaxError, LPSemanticError


class FileCompiler(object):
    def __init__(self, source):
        self.source = source
        self.blocks = None

        self._grab_blocks()
        if not self.blocks.get('_main'):
            raise LPSemanticError('Source file must define _main block')

        self.process_block_references('_main')

    def output(self):
        return self.blocks['_main']

    def _grab_blocks(self):
        """
        Parse `self.source` and return a dict mapping block names to their
        raw content.
        """
        r = BlockRecordRenderer()
        mistune.markdown(self.source, renderer=r)
    
        blocks = {}
        for block in r.blocks:
            name, content = self._parse_raw_block(block)
            blocks[name] = content        
        self.blocks = blocks
    
    def process_block_references(self, name):
        self.blocks[name] = self._process_block_references(
            name,
            self.blocks[name],
        )

    def _process_block_references(self, name, content):
        """
        Resolve references within a block recursively.
        """
        lines = content.splitlines()
        new_lines = []
        for line in lines:
            if not line.lstrip().startswith('%'):
                new_lines.append(line)
                continue

            # Count the indentation level of this line
            # TODO - Support tabs
            # TODO - Error on mixed tabs
            indent = line[:line.index('%')].count(' ')

            # Get the name of the referenced block, and grab its contents
            # from self.blocks
            ref_name = line.strip().lstrip('%')
            ref_content = self.blocks.get(ref_name)
            if not ref_content: 
                raise LPSemanticError('Invalid ref: {}'.format(ref_name))

            # Recursively resolve the referenced block's references
            ref_content = self._process_block_references(ref_name, ref_content)

            # Append `ref_content` to `new_lines` line-by-line, preserving the
            # indentation level of the current block.
            for rcl in ref_content.splitlines():
                rcl = (' ' * indent) + rcl
                new_lines.append(rcl)

        return '\n'.join(new_lines)

    def _parse_raw_block(self, raw_block):
        """
        Split a block's name from its content.
        """
        lines = raw_block.splitlines()
        if len(lines) < 2:
            raise LPSyntaxError('Invalid block - must not be empty')
        if not lines[0].startswith('$'):
            raise LPSyntaxError('Invalid block - must start with name')
    
        name = lines[0].strip('$').strip()
        content = '\n'.join(lines[1:]).strip()
        return name, content


class BlockRecordRenderer(mistune.Renderer):
    """
    To extract code blocks from Markdown source, we use `mistune` and this
    custom renderer.

    BlockRecordRenderer doesn't actually render code blocks, it just saves
    their content in a list internally. This list is later read by `FileParser`
    """
    def __init__(self, *args, **kwargs):
        super(BlockRecordRenderer, self).__init__(*args, **kwargs)
        self.blocks = []

    def block_code(self, code, lang):
        self.blocks.append(code)
        return ''
