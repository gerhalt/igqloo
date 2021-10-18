#!/usr/bin/env python3
"""A small command-line tool for easily writing GQL queries.
"""
import re
import requests
import sys
from argparse import ArgumentParser


class Node(object):
    """Represents a node in a GraphQL query tree
    """
    def __init__(self, name=None, alias=None, root=True):
        self.name = name
        self.alias = alias
        self.root = root
        self.filters = {}
        self.children = {}

    def __getitem__(self, name):
        """Finds a node in the tree based on the path. Side effect: if a node
        isn't found in the path, it will be created.
        """
        node = self
        for segment in name.split('.'):
            if segment not in node.children:
                # TODO: Check for aliases in children before creating a new node
                node.children[segment] = Node(name=segment, root=False)
            node = node.children[segment]

        return node

    def __setitem__(self, name, value):
        self[name].fields.update(value)

    def __str__(self):
        """Returns a query string from this node and its children
        """
        query = []

        if self.root:
            query.append('query')

        if self.alias is not None:
            query.append(self.alias + ':')

        if self.name is not None:
            query.append(str(self.name))

        if self.filters:
            query.append('(')
            for k,v in self.filters.items():
                query.append('{k}:"{v}"'.format(k=k, v=v))
            query.append(')')

        if self.children:
            query.append('{')
            if self.children:
                for idx, f in enumerate(self.children.values()):
                    query.append(str(f))
                    if idx < len(self.children) - 1:
                        query.append(',')

            query.append('}')

        return ''.join(query)

    def add_filters(self, **kwargs):
        self.filters.update(kwargs)


def parse_fields(q, fields):
    """Parse out a list of fields, adding them to the query.
    """
    for f in fields:
        current_node = q
        last_idx = 0
        quoted = False
        segment_chunks = []

        for idx, c in enumerate(f):
            if idx == len(f) - 1:
                segment_chunks.append(f[last_idx:])
            elif c in {',', '.', '('} and not quoted:
                if idx > last_idx + 1:
                    segment_chunks.append(f[last_idx:idx])
                last_idx = idx
            elif c in {')'} and idx > last_idx + 1:
                segment_chunks.append(f[last_idx:idx + 1])
                last_idx = idx

            if c == '(' and not quoted:
                quoted = True
            elif c == ')' and quoted:
                quoted = False

            if c == '.' and not quoted or idx == len(f) - 1:
                parent_node = current_node
                for chunk in segment_chunks:
                    if chunk[0] == '.':
                        current_node = current_node[chunk[1:]]
                    elif chunk[0] == ',':
                        current_node = parent_node[chunk[1:]]
                    elif chunk[0] == '(':
                        chunk = chunk[1:-1]
                        if ' as ' in chunk.lower():
                            split = chunk.lower().index(' as ')
                            name = chunk[:split]
                            alias = chunk[split+4:]
                            current_node = current_node[name]
                            current_node.alias = alias
                        else:
                            k,v = chunk.split(':', 1)
                            current_node.add_filters(**{k:v})
                    else:
                        current_node = current_node[chunk]

                segment_chunks = []

    return q


def main():
    parser = ArgumentParser(
            description='Interact with a GQL query.')
    parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Enable verbose output')
    parser.add_argument(
            'uri',
            help='URI of GraphQL interface')
    parser.add_argument(
            'fields',
            nargs='+',
            help='Fields to request')

    args = parser.parse_args()

    q = Node(root=True)
    q = parse_fields(q, args.fields)

    if args.verbose:
        print(q)

    resp = requests.get(args.uri, params={'query': q})
    data = resp.json()

    if 'errors' in data:
        for err in data['errors']:
            print(err['message'])
        sys.exit(1)
    else:
        print(resp.text)


if __name__ == '__main__':
    test()
