from gostep.consts import CMD_TREE, VALIDATION_MESSAGES, TYPE, TEXT, REQUIRED_FIELDS, BOOLEAN, CMD_BRANCHES, COMMANDS


def print_messages(msgs):
    for line in msgs:
        print(line)


def validate_fields(arg_schema_branch, args):
    if len(arg_schema_branch[REQUIRED_FIELDS]) != 0:
        if isinstance(arg_schema_branch[REQUIRED_FIELDS], dict):
            arg_schema_field_keys = arg_schema_branch[REQUIRED_FIELDS].keys()
            if not all(i in args for i in arg_schema_field_keys):
                print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                return False
            for field_key in arg_schema_field_keys:
                if arg_schema_branch[REQUIRED_FIELDS][field_key][TYPE] == TEXT:
                    field_arg_index = args.index(field_key)
                    if field_arg_index == len(args) - 1 or args[field_arg_index + 1] in COMMANDS:
                        print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                        return False
        if isinstance(arg_schema_branch[REQUIRED_FIELDS], list):
            arg_schema_field_keys = [list(key.keys())[0] for key in arg_schema_branch[REQUIRED_FIELDS]]
            if not any(i in args for i in arg_schema_field_keys):
                print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                return False
            if all(i in args for i in arg_schema_field_keys):
                print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                return False
            for arg in arg_schema_field_keys:
                index = args.index(arg)
                if args[index != len(args) - 1] and args[index + 1] not in COMMANDS:
                    print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                    return False
            return True
    return True


def validated(args=None):
    if args is None or len(args) <= 1:
        print_messages(CMD_TREE[VALIDATION_MESSAGES])
        return False
    if len(args) != len(set(args)):
        print_messages(
            [
                'Error: Gostep key words are not allowed to be used as variable names.',
                'Gostep keys:',
                '  ' + ', '.join(COMMANDS)
            ]
        )
        return False
    for arg_index in range(0, len(args)):
        if args[arg_index] in CMD_BRANCHES:
            arg_schema = CMD_TREE[args[arg_index]]
            if arg_index == len(args) - 1 and arg_schema[TYPE] == BOOLEAN:
                return True
            for arg_schema_key in arg_schema.keys():
                if arg_schema_key == VALIDATION_MESSAGES:
                    continue
                elif arg_schema_key == TYPE:
                    index = args.index(args[arg_index])
                    if arg_schema[arg_schema_key] == TEXT:
                        if index == len(args) - 1 or args[index + 1] in COMMANDS:
                            print_messages(arg_schema[VALIDATION_MESSAGES])
                            return False
                    elif arg_schema[arg_schema_key] == BOOLEAN and args[index + 1] in COMMANDS and args[index + 1] in arg_schema.keys() and arg_schema[args[index + 1]][TYPE] == BOOLEAN:
                        return True
                elif arg_schema_key == REQUIRED_FIELDS:
                    if not validate_fields(arg_schema, args):
                        return False
                    return True
                else:
                    if not arg_schema_key in args:
                        print_messages(arg_schema[VALIDATION_MESSAGES])
                        return False
                    else:
                        arg_schema_branch = arg_schema[arg_schema_key]
                        if arg_schema_branch[TYPE] == TEXT:
                            branch_index = args.index(arg_schema_key)
                            if branch_index == len(args) - 1 or args[branch_index + 1] in CMD_BRANCHES:
                                print_messages(arg_schema_branch[VALIDATION_MESSAGES])
                                return False
                            validate_fields(arg_schema_branch, args)
                        elif arg_schema_branch[TYPE] == BOOLEAN:
                            continue
            return True
    print_messages(CMD_TREE[VALIDATION_MESSAGES])
    return False
