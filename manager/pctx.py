import argparse

from cloudify_cli.cli import cfy


def _get_resolver_rules(pctx):
    return pctx['context']['cloudify']['import_resolver']['parameters']['rules']


def _set_resolver_rules(pctx, rules):
    pctx['context']['cloudify']['import_resolver']['parameters']['rules'] = rules


def _update_context(client, ctx):
    client.manager.update_context('provider', ctx['context'])


@cfy.pass_client()
def pctx_get(client, **_):
    ctx = client.manager.get_context()
    print str(ctx)


@cfy.pass_client()
def get_resolver_rules(client, **_):
    ctx = client.manager.get_context()
    rules = _get_resolver_rules(ctx)
    rules_dict = dict()
    for rule in rules:
        rules_dict.update(rule)
    for x, y in rules_dict.iteritems():
        print "{} -> {}".format(x, y)


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


@cfy.pass_client()
def set_resolver_rule(client, src, dest, **_):
    ctx = client.manager.get_context()
    rules = _get_resolver_rules(ctx)
    for rule in rules:
        s, _ = rule.iteritems().next()
        if s == src:
            rule[src] = dest
            break
    else:
        rules.append({src: dest})
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

    rr_remove_parser = resolver_rules_sp.add_parser('remove')
    rr_remove_parser.add_argument('src')
    rr_remove_parser.set_defaults(func=remove_resolver_rule)

    rr_set_parser = resolver_rules_sp.add_parser('set')
    rr_set_parser.add_argument('src')
    rr_set_parser.add_argument('dest')
    rr_set_parser.set_defaults(func=set_resolver_rule)

    args = master_parser.parse_args()
    args.func(**vars(args))
