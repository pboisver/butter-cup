from typing import Annotated, Optional

import uvicorn
from typer import Argument, Typer

from butter_cup import flower

cli = Typer(no_args_is_help=True)


@cli.command()
def foo(pad_to: Annotated[Optional[int], Argument()] = 42) -> str:
    return flower(pad_to)


@cli.command()
def bar(pad_to: Annotated[Optional[int], Argument()] = 42) -> str:
    return flower(pad_to * 2)


@cli.command()
def web():
    uvicorn.run("butter_cup.api:app", reload=True, use_colors=True)

# Notes
# web api and cli api
# each of those could handle json input and csv input
# json and csv formats could allow individual or bulk
#
# in the CLI processing we should allow a single file (csv) with multiple performers
#
# we might want to allow the web interface to ingest a bulk file (csv) as well

