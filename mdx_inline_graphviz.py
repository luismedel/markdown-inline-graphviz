"""
Graphviz extensions for Markdown.
Renders the output inline, eliminating the need to configure an output
directory.

Supports outputs types of SVG and PNG. The output will be taken from the
filename specified in the tag. Example:

{% dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
%}

Requires the graphviz library (http://www.graphviz.org/)

Inspired by jawher/markdown-dot (https://github.com/jawher/markdown-dot)
"""

import re
import base64
import markdown
import subprocess

import typing as t

# Global vars
BLOCK_RE: re.Pattern = re.compile(
    r"^\{% (?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)%}\s*$", re.MULTILINE | re.DOTALL
)

FENCES_RE: re.Pattern = re.compile(
    r"^```\s*graphviz\s+(?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)```\s*$", re.MULTILINE | re.DOTALL
)

# Command whitelist
SUPPORTED_COMMAMDS: t.List[str] = ["dot", "neato", "fdp", "sfdp", "twopi", "circo"]
SUPPORTED_FILETYPES: t.List[str] = ["svg", "png"]


class InlineGraphvizExtension(markdown.Extension):
    def extendMarkdown(self, md: markdown.Markdown):
        """Add InlineGraphvizPreprocessor to the Markdown instance."""
        md.registerExtension(self)
        md.preprocessors.register(InlineGraphvizPreprocessor(md), "graphviz_block", 1.0)


class InlineGraphvizPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md: markdown.Markdown):
        super(InlineGraphvizPreprocessor, self).__init__(md)

    def run(self, lines: t.List[str]):
        """Match and generate dot code blocks."""

        text = "\n".join(lines)
        text_offset: int = 0

        while True:
            m_block: re.Match | None = BLOCK_RE.search(text, text_offset)
            m_fences: re.Match | None = FENCES_RE.search(text, text_offset)
            if not m_block and not m_fences:
                break

            m: re.Match
            if not m_block:
                m = m_fences
            elif not m_fences:
                m = m_block
            else:
                m = m_block if m_block.start() < m_fences.start() else m_fences

            command = m.group("command")
            if command not in SUPPORTED_COMMAMDS:
                raise Exception(f"Command not supported: {command}")

            filename = m.group("filename")
            content = m.group("content")

            filetype = filename[filename.rfind(".") + 1 :]
            if filetype not in SUPPORTED_FILETYPES:
                raise Exception(f"File type not supported: {filetype}")

            args = [command, "-T" + filetype]
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            proc.stdin.write(content.encode("utf-8"))

            output, _ = proc.communicate()

            if filetype == "svg":
                data_url_filetype = "svg+xml"
                encoding = "utf-8"
                graph = output.decode(encoding)
            elif filetype == "png":
                data_url_filetype = "png"
                encoding = "base64"
                output = base64.b64encode(output)
                data_path = "data:image/%s;%s,%s" % (data_url_filetype, encoding, output)
                graph = "![" + filename + "](" + data_path + ")"

            text = "%s\n%s\n%s" % (text[: m.start()], graph, text[m.end() :])
            text_offset = m.end()

        return text.split("\n")


def makeExtension(*args, **kwargs):
    return InlineGraphvizExtension(*args, **kwargs)
