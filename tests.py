import markdown


def test_render_backtick_fences() -> None:
    input = """
Hi there!

```graphviz dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
```
"""

    output = markdown.markdown(input, extensions=["mdx_inline_graphviz"])

    assert "Hi there!" in output, output
    assert "<svg" in output, output


def test_render_tilde_fences() -> None:
    input = """
Hi there!

```graphviz dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
```
"""

    output = markdown.markdown(input, extensions=["mdx_inline_graphviz"])

    assert "Hi there!" in output, output
    assert "<svg" in output, output


def test_detect_unknown_command() -> None:
    input = """
Hi there!

```graphviz unknown attack_plan.svg
    digraph G {
    }
```
"""

    try:
        _ = markdown.markdown(input, extensions=["mdx_inline_graphviz"])
        raise AssertionError("You should not see this")
    except Exception as ex:
        assert str(ex) == "Command not supported: unknown"


def test_detect_unknown_filetype() -> None:
    input = """
Hi there!

```graphviz dot attack_plan.zip
    digraph G {
    }
```
"""

    try:
        _ = markdown.markdown(input, extensions=["mdx_inline_graphviz"])
        raise AssertionError("You should not see this")
    except Exception as ex:
        assert str(ex) == "File type not supported: zip"
