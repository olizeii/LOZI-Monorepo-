"""Start: `python -m lozi_core` bzw. `lozi-core`."""
from __future__ import annotations

import logging

import uvicorn

from .app import baue_app
from .config import Config


def main() -> None:
    config = Config.aus_umgebung()
    logging.basicConfig(level=config.log_level, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    app, _, _ = baue_app(config)
    logging.getLogger("lozi").info(
        "Lozi-Core startet auf %s:%d – Displays: %s", config.host, config.port, ", ".join(config.displays)
    )
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level.lower())


if __name__ == "__main__":
    main()
