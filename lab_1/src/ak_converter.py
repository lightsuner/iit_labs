from collections import deque
import copy

tags = {
    'head': 'h1',
    'block': 'div',
    'paragraph': 'p',
    'list': 'ul',
    'item': 'li',
    'link': 'a',
    'picture': 'img',
    'newline': 'br',
    'bold': 'b',
    'italic': 'i',
    'underscore': 'u',
    'strike': 's',
}

escape_chars = {
    '&hash;': '#',
}

html_escape_chars = {
    '<': '&lt',
    '>': '&gt',
    '&': '&amp;'
}

class AKConverter:
    def to_html(self, data):
        data_copy = copy.deepcopy(data)

        # expand data
        oq = deque()
        oq.append(data_copy)

        while True:
            if not oq:
                break

            node = oq.popleft()
            node.closed = False

            children = node.children

            if children:
                for c in children:
                    oq.append(c)

        q = deque()
        q.append(data_copy)

        output = []

        while True:
            if not q:
                break

            node = q.pop()
            tag = node.tag

            if tag:
                tag = tag.lower()

                if 'link' == tag:
                    output.append(self.make_a(node))
                    continue

                if 'picture' == tag:
                    output.append(self.make_img(node))
                    continue

                html_tag = tags[tag]
                if html_tag:
                    html_tag = html_tag.lower()
                    if not node.closed:
                        output.append(f'<{html_tag}>')
                    else:
                        output.append(f'</{html_tag}>')

            if node.closed:
                continue
            else:
                node.closed = True

            children = node.children

            if children:
                q.append(node)
                for c in reversed(children):
                    q.append(c)
            else:
                if node.value:
                    output.append(self.escape_all(node.value).strip())

        return "\n".join(output)

    def make_a(self, node):
        ch = node.children

        html_tag = ''

        if len(ch) > 0 and ch[0].value:
            link_values = ch[0].value.split('|')
            link = link_values[0]
            title = link_values[0]

            if len(link_values) > 1:
                link = link_values[1]

            html_tag = f'<a href="{self.escape(link).strip()}">' \
                       f'{self.escape_all(title).strip()}</a>'

        return html_tag

    def make_img(self, node):
        ch = node.children

        html_tag = ''

        if len(ch) > 0 and ch[0].value:
            html_tag = f'<img src="{self.escape(ch[0].value).strip()}">'

        return html_tag

    def escape_all(self, value):
        value = self.escape_html(value)
        value = self.escape(value)
        return value

    def escape(self, value):
        for v, e in escape_chars.items():
            value = value.replace(v, e)
        return value

    def escape_html(self, value):
        for v, e in html_escape_chars.items():
            value = value.replace(v, e)
        return value
