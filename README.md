# Markdown Inline Graphviz

> Note: This is a fork of the [Markdown Inline Graphviz extension by Steffen Prince](https://github.com/sprin/markdown-inline-graphviz) with additional syntax support and minor modifications.

A Python Markdown extension that replaces inline Graphviz definitions with inline SVGs or PNGs!

Why render the graphs inline? No configuration! Works with any Python-Markdown-based static site generator, such as
[MkDocs](http://www.mkdocs.org/), [Pelican](http://blog.getpelican.com/), and [Nikola](https://getnikola.com/) out of the box without configuring an output directory.

## Installation

```sh
$ pip install git+https://github.com/luismedel/markdown-inline-graphviz
```

## Usage

Activate the `mdx_inline_graphviz` extension. For example, with Mkdocs, you add a stanza to `mkdocs.yml`:

```yaml
markdown_extensions:
    - mdx_inline_graphviz
```

To use it in your Markdown doc:

<pre>
```graphviz dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
```
</pre>

...or using tilde fences...

```markdown
~~~graphviz dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
~~~
```

Supported graphviz commands: `dot`, `neato`, `fdp`, `sfdp`, `twopi`, `circo`.

## Credits

Inspired by [jawher/markdown-dot](https://github.com/jawher/markdown-dot), which renders the dot graph to a file instead of inline.

## License

[MIT License](http://www.opensource.org/licenses/mit-license.php)
