def cli_main(build_argument_parser, run):
    """
    Parse the provided command-line arguments and
    pass them to the current script run function

    :param build_argument_parser: Return argument parser
    :param run: Run current script
    """

    arg_parser = build_argument_parser()
    args = arg_parser.parse_args()
    cli_params = vars(args)

    run_params = {}
    for cli_param in cli_params:
        if cli_param in run.__code__.co_varnames:
            run_params[cli_param] = cli_params[cli_param]

    run(**run_params)

