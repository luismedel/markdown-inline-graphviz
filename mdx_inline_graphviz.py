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

REGEXPS: t.List[re.Pattern] = [
    # backtick fences
    re.compile(
        r"^```\s*graphviz\s+(?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)```\s*$",
        re.MULTILINE | re.DOTALL,
    ),
    # tilde fences
    re.compile(
        r"^~~~\s*graphviz\s+(?P<command>\w+)\s+(?P<filename>[^\s]+)\s*\n(?P<content>.*?)~~~\s*$",
        re.MULTILINE | re.DOTALL,
    ),
]

VALID_COMMAMDS: t.List[str] = ["dot", "neato", "fdp", "sfdp", "twopi", "circo"]

VALID_FILETYPES: t.List[str] = ["svg", "png"]


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
            m: re.Match | None = None
            for r in REGEXPS:
                tmp = r.search(text, text_offset)
                if not tmp:
                    continue
                if not m or tmp.start() < m.start():
                    m = tmp

            if not m:
                break

            command = m.group("command")
            if command not in VALID_COMMAMDS:
                raise Exception(f"Command not supported: {command}")

            filename = m.group("filename")
            content = m.group("content")

            filetype = filename[filename.rfind(".") + 1 :]
            if filetype not in VALID_FILETYPES:
                raise Exception(f"File type not supported: {filetype}")

            args = [command, "-T" + filetype]
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            proc.stdin.write(content.encode())
            output, _ = proc.communicate()

            graph: str

            if filetype == "svg":
                graph = output.decode()
                # Strip any garbage outside the svg tag
                svg_pos = graph.index("<svg")
                if svg_pos != -1:
                    graph = graph[svg_pos:]
            elif filetype == "png":
                b64 = base64.b64encode(output)
                data_path = f"data:image/png;base64,{b64}"
                graph = f'<img src="{data_path}" title="{filename}" />'

            text = "%s\n%s\n%s" % (text[: m.start()], graph, text[m.end() :])
            text_offset = m.end()

        return text.split("\n")


def makeExtension(*args, **kwargs):
    return InlineGraphvizExtension(*args, **kwargs)
