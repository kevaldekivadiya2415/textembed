"""Async engine array."""

from typing import Iterable, Iterator, List, Union

from .args import AsyncEngineArgs
from .async_engine import AsyncEngine


class AsyncEngineArray:
    """AsyncEngineArray is a collection of AsyncEngine objects."""

    def __init__(self, engines: Iterable["AsyncEngine"]):
        if not engines:
            raise ValueError("Engines collection cannot be empty.")
        unique_model_names = set(
            engine.engine_args.served_model_name for engine in engines
        )
        if len(list(engines)) != len(unique_model_names):
            raise ValueError("Each engine must have a unique served model name.")
        self.engines_dict = {
            engine.engine_args.served_model_name: engine for engine in engines
        }

    @classmethod
    def from_args(
        cls, engine_args_list: Iterable[AsyncEngineArgs]
    ) -> "AsyncEngineArray":
        """Create an AsyncEngineArray from a list of AsyncEngineArgs.

        Args:
            engine_args_list (Iterable[AsyncEngineArgs]): List of AsyncEngineArgs objects.

        Returns:
            AsyncEngineArray: An instance of the AsyncEngineArray class.
        """
        engines = map(AsyncEngine.from_args, engine_args_list)
        return cls(engines=tuple(engines))

    @property
    def engine_args(self) -> List[AsyncEngineArgs]:
        """Get the engine arguments for all engines.

        Returns:
            List[AsyncEngineArgs]: List of AsyncEngineArgs for all engines.
        """
        return [engine.engine_args for engine in self.engines_dict.values()]

    def __iter__(self) -> Iterator["AsyncEngine"]:
        return iter(self.engines_dict.values())

    async def start_all(self):
        """Start up all engines asynchronously."""
        for engine in self.engines_dict.values():
            await engine.start()

    async def stop_all(self):
        """Stop all engines asynchronously."""
        for engine in self.engines_dict.values():
            await engine.stop()

    def __getitem__(self, key: Union[str, int]) -> "AsyncEngine":
        """Retrieve an engine by model name or index. Auto resolve if only one engine is present.

        Args:
            key (Union[str, int]): Model name or index to be used.

        Returns:
            AsyncEngine: The resolved AsyncEngine instance.

        Raises:
            IndexError: If the engine for the specified model name is not found.
        """
        if len(self.engines_dict) == 1:
            return list(self.engines_dict.values())[0]
        if isinstance(key, int):
            return list(self.engines_dict.values())[key]
        if isinstance(key, str) and key in self.engines_dict:
            return self.engines_dict[key]
        raise IndexError(
            f"Engine for model name `{key}` not found. "
            f"Available model names are {list(self.engines_dict.keys())}."
        )
