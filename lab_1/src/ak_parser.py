from ak_node import AKNode
import code

OPEN_TAG = '#'
CLOSE_TAG = '#'

class AKParser:
    def reset(self):
        self.index = 0
        self.root = None
        self.content = None

    def parse(self, path):
        self.reset()

        with open(path, encoding='utf8') as f:
            content = ' '.join(f.read().splitlines())
            self.content = ' '.join(content.split())

        self.parse_tree()

        return self.root

    def parse_tree(self, parent_node=None):
        while True:
            open_tag = self.parse_open_tag()

            if open_tag:
                node = AKNode()
                node.tag = open_tag

                if open_tag == 'newline' and not parent_node:
                    continue

                if parent_node:
                    parent_node.children.append(node)
                else:
                    self.root = node

                if open_tag == 'newline':
                    continue

                self.parse_tree(node)

            value = self.parse_value()
            if value:
                node = AKNode()
                node.value = value
                parent_node.children.append(node)

            close_tag = self.parse_close_tag()
            if close_tag and parent_node.tag == close_tag:
                parent_node.closed = True
                return

            if not open_tag and not value and not close_tag:
                return

    def parse_open_tag(self):
        open_tag = ''
        is_open_tag = False
        index = self.index

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return
            c = c.strip()

            if not is_open_tag and c == OPEN_TAG:
                is_open_tag = True
                index += 1
                continue

            if not is_open_tag and c != OPEN_TAG:
                return None

            if is_open_tag and not c:
                index += 1
                break

            if is_open_tag:
                index += 1
                open_tag += c

        self.index = index
        return open_tag

    def parse_value(self):
        value = ''
        index = self.index

        tmp_val = ''

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return

            if c == OPEN_TAG:
                break

            if c == CLOSE_TAG:
                break

            index += 1
            tmp_val += c

            # save current values
            if c == ' ':
                self.index = index
                value += tmp_val
                tmp_val = ''

        return value

    def parse_close_tag(self):
        close_tag = ''
        index = self.index

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return

            if c == ' ':
                return None

            if c == CLOSE_TAG:
                if close_tag:
                    index += 1
                break

            index += 1
            close_tag += c

        self.index = index
        return close_tag

    def has_next(self):
        return self.index < len(self.content)
