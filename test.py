import markdown

def test_render_block() -> None:
    input = """
Hi there!

{% dot attack_plan.svg
    digraph G {
        rankdir=LR
        Earth [peripheries=2]
        Mars
        Earth -> Mars
    }
%}
"""

    output = markdown.markdown(input, extensions=["mdx_inline_graphviz"])

    assert "Hi there!" in output, output
    assert "<svg" in output, output
