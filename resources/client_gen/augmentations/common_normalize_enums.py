#!/usr/bin/env python3
import json, sys

def split(enum_list):
    if isinstance(enum_list, list) and len(enum_list) == 1 and isinstance(enum_list[0], str) and "," in enum_list[0]:
        return [p.strip() for p in enum_list[0].split(',') if p.strip()]
    return enum_list

def dedupe(seq):
    seen = set(); out = []
    for item in seq:
        key = json.dumps(item, sort_keys=True) if not isinstance(item, (str, int, float, bool, type(None))) else item
        if key not in seen:
            seen.add(key); out.append(item)
    return out

def walk(node):
    if isinstance(node, dict):
        if 'enum' in node and isinstance(node['enum'], list):
            node['enum'] = dedupe(split(node['enum']))
        for k, v in list(node.items()):
            node[k] = walk(v)
        return node
    if isinstance(node, list):
        return [walk(x) for x in node]
    return node

def main():
    if len(sys.argv) != 3:
        print('Usage: common_normalize_enums.py <input.json> <output.json>')
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    data = walk(data)
    with open(sys.argv[2], 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    main()

