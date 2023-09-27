from discord_lambda import Interaction, Embedding, CommandArg, CommandRegistry
import time


def test_command(inter: Interaction, input: str) -> None:
    inter.send_response(content=f"Hello, {input}",
                        embeds=[Embedding(title="Test",
                                          desc="This is a test embed!",
                                          footer=f"Request completed in {round(time.time() - inter.timestamp, 2)}s")])


def setup(registry: CommandRegistry) -> None:
    registry.register_cmd(func=test_command, name="test", desc="Test command", options=[
        CommandArg(name="input", desc="Add some input to the command!", type=CommandArg.Types.STRING)
    ])