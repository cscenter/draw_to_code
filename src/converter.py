class Converter:
    def convert(self, figures):
        raise NotImplementedError


class TexConverter(Converter):

    template = """
    \\begin{{tikzpicture}}[scale = 0.5]
        {}
    \\end{{tikzpicture}}
    """

    def convert(self, figures):
        tex_figures = [figure.to_tex() for figure in figures]
        return self.template.format("\n".join(tex_figures))
