#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import (
    Engine,
    create_engine,
)

import argparse
import argcomplete
import model as MD
import dispatcher as D


parser = argparse.ArgumentParser(
    description="Do [some actions] on workout_model",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--permanent-db", default="workout_model2_db.db", help="what db file to use"
)
parser.add_argument("--memory-db", help="use memory db")
parser.add_argument(
    "--echo", help="Show db commands", action="store_true", default=False
)


if __name__ == "__main__":
    parser.add_argument(
        "command",
        nargs="+",
        choices=D.Dispatcher.ensure_commands_collected(),
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine: Engine
    if args.memory_db:
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            echo=args.echo,
            future=True,
        )
    elif args.permanent_db:
        engine = create_engine(
            f"sqlite+pysqlite:///{args.permanent_db}",
            echo=args.echo,
            future=True,
        )
    else:
        raise RuntimeError("--permanent-db or --memory-db expected")

    MD.Base.metadata.create_all(engine)
    with MD.Session(engine) as session:
        dispatcher: D.Dispatcher = D.Dispatcher(session)
        for cmd_name in args.command:
            getattr(dispatcher, cmd_name)()
