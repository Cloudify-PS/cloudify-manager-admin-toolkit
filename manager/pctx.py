#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
from collections import OrderedDict

from cloudify_cli.cli import cfy

DEFAULT_RULES = OrderedDict({
    "http://www.getcloudify.org/spec": "file:///opt/manager/resources/spec",
    "http://cloudify.co/spec": "file:///opt/manager/resources/spec",
    "https://www.getcloudify.org/spec": "file:///opt/manager/resources/spec",
    "https://cloudify.co/spec": "file:///opt/manager/resources/spec",
})

def _get_resolver_rules(pctx):
    return pctx['context']['cloudify']['import_resolver']['parameters']['rules']


def _set_resolver_rules(pctx, rules):
    pctx['context']['cloudify']['import_resolver']['parameters']['rules'] = rules


def _update_context(client, ctx):
    client.manager.update_context('provider', ctx['context'])


def _rules_to_ordered_dict(ctx):
    rules = _get_resolver_rules(ctx)
    rules_dict = OrderedDict()
    for rule in rules:
        src, dest = rule.iteritems().next()
        rules_dict[src] = dest
    return rules_dict


def _ordered_dict_to_rules(rules_dict):
    lst = list()
    for x, y in rules_dict.items():
        lst.append({x: y})
    return lst


@cfy.pass_client()
def pctx_get(client, **_):
    ctx = client.manager.get_context()
    print(str(ctx))


@cfy.pass_client()
def get_resolver_rules(client, **_):
    ctx = client.manager.get_context()
    rules_dict = _rules_to_ordered_dict(ctx)
    for x, y in rules_dict.items():
        print("{} -> {}".format(x, y))


@cfy.pass_client()
def remove_resolver_rule(client, src, **_):
    ctx = client.manager.get_context()
    rules = _get_resolver_rules(ctx)
    updated_rules = []
    for rule in rules:
        s, _ = rule.iteritems().next()
        if s != src:
            updated_rules.append(rule)
    _set_resolver_rules(ctx, updated_rules)
    _update_context(client, ctx)


def _build_resolver_rules(rules):
    rules_dict = OrderedDict()
    rules_dict.update(DEFAULT_RULES)
    for item in rules:
        src, dest = item.iteritems().next()
        rules_dict[src] = dest

    return rules_dict


@cfy.pass_client()
def set_resolver_rule(client, src, dest, data, dry_run, **_):
    ctx = client.manager.get_context()

    if data:
        with open(data, 'r') as f:
            data_json = json.load(f)
        rules_dict = _build_resolver_rules(data_json)
    else:
        rules_dict = _rules_to_ordered_dict(ctx)
        rules_dict[src] = dest

    rules = _ordered_dict_to_rules(rules_dict)
    print("Updated rules:\n%s" % json.dumps(rules, indent=4))
    if not dry_run:
        _set_resolver_rules(ctx, rules)
        _update_context(client, ctx)


@cfy.pass_client()
def reset_resolver_rules(client, **_):
    ctx = client.manager.get_context()
    rules_dict = _build_resolver_rules([])
    rules = _ordered_dict_to_rules(rules_dict)
    _set_resolver_rules(ctx, rules)
    _update_context(client, ctx)


if __name__ == '__main__':
    master_parser = argparse.ArgumentParser()
    subparsers = master_parser.add_subparsers()
    subparsers.required = True

    get_parser = subparsers.add_parser('get')
    get_parser.set_defaults(func=pctx_get)

    resolver_rules_parser = subparsers.add_parser('resolver-rules')
    resolver_rules_sp = resolver_rules_parser.add_subparsers()

    rr_get_parser = resolver_rules_sp.add_parser('get')
    rr_get_parser.set_defaults(func=get_resolver_rules)

    rr_reset_parser = resolver_rules_sp.add_parser('reset')
    rr_reset_parser.set_defaults(func=reset_resolver_rules)

    rr_remove_parser = resolver_rules_sp.add_parser('remove')
    rr_remove_parser.add_argument('src')
    rr_remove_parser.set_defaults(func=remove_resolver_rule)

    rr_set_parser = resolver_rules_sp.add_parser('set')
    rr_set_parser.add_argument('-n', '--dry-run', action='store_true', default=False)
    rr_set_parser.add_argument('--src')
    rr_set_parser.add_argument('--dest')
    rr_set_parser.add_argument('--data')
    rr_set_parser.set_defaults(func=set_resolver_rule)

    args = master_parser.parse_args()
    args.func(**vars(args))
