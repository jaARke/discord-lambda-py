# Discord Lambda Py
A template for Discord bot creation using AWS Lambda and API Gateway. This project attempts to offer similar functionality as the [`slash-create`](https://github.com/Snazzah/slash-create) JavaScript library but in a serverless, Python environment.

An example project leveraging this template can be found [here](https://github.com/UF-ACE/stock-prediction).

## Setup
To get started quickly, watch this [video walkthrough](https://www.youtube.com/watch?v=iUAjpSlJrgU), which shows each of the setup steps described below.
### Discord
1. Activate developer mode on your Discord account.
2. Create a new application [here](https://discord.com/developers/applications).
3. Copy your Application ID and Public Key and save them for later.
3. Navigate to the "Bot" tab and select "Reset Token".
4. Copy your bot's token and save it for later.
5. Navigate to the "Oauth2" tab and select "URL Generator".
6. Select the `applications.commands` scope and paste the generated URL into your browser.
7. Add your bot to your desired server.

### AWS
1. Follow [this tutorial](https://oozio.medium.com/serverless-discord-bot-55f95f26f743) to setup the Lambda environment, but do not add any code to the default Lambda function. This will be done automatically by the template.
    * Set your API Gateway endpoint type to edge-optimized to avoid timeout errors.
    * Make note of your API endpoint.
2. Follow [this tutorial](https://medium.com/@shamnad.p.s/how-to-create-an-s3-bucket-and-aws-access-key-id-and-secret-access-key-for-accessing-it-5653b6e54337) to setup an S3 bucket and keys for accessing it. Be sure to:
    * Give the IAM user full access to S3.
    * Copy the Access Key ID and secret access key and save them for later.
    * Copy the S3 bucket's name and URI (s3://<bucket-name>) and save it for later.

### GitHub
1. Create a new repository using this template.
2. Add the following to your repository's secrets (under "Settings" -> "Secrets").
    * `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID.
    * `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.
    * `APP_ID`: The ID of your Discord application.
    * `PUBLIC_KEY`: The public key of your Discord application.
    * `BOT_TOKEN`: The token of your Discord bot.
2. Clone your new repository.
3. Fill out necessary fields in `.github/workflows/awsLambda.yml`. These fields are marked with `TODO` comments.
    * See [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) for a list of region codes.
4. Push your changes to GitHub. This will trigger the workflow, which will deploy your Lambda function if everything is setup correctly.

Once your function is deployed, navigate back to the Discord Developer Portal and paste your API endpoint into the "Interactions Endpoint URL" field on your application's homepage. You should now be able to issue commands in the server you added the bot to.

## Development
### Adding Commands
1. Create a new file in the `commands` directory.
2. Create command functions in the file with the following signature:
    ```python
    def command_name(interaction: Interaction) -> None:
        ...
    ```
    * `interaction` is an `Interaction` object containing information about the command's context. See Class Reference below for more information.
    * Further arguments can be added to the function signature to allow the command to receive options.
3. Create a function in the file with the following signature:
    ```python
    def setup(registry: CommandRegistry) -> None:
        ...
    ```
4. Use the `registry` object to register your command functions. See Class Reference below for more information.

### Using Python Packages
Any additional packages leveraged by your commands should be added to `requirements.txt`. The deployment workflow will automatically upload these packages as a layer to your Lambda function.

### Using Environment Variables
If your custom commands require environment variables, follow these steps:

1. Add your environment variables as GitHub secrets on your repository.
2. Add those variables below [this line](https://github.com/jaARke/discord-lambda-py/blob/6712bd3a5e4b2fb69380898bc6b3f756205f4e08/.github/workflows/awsLambda.yml#L90) in `.github/workflows/awsLambda.yml`.
3. Access your environment variables in your commands using `os.environ.get("ENV_VAR_NAME")`.

This will ensure that your variables are forwarded to the Lambda function when it is deployed.

### Syncing to this Template
This template provides a workflow, `.github/workflows/syncToTemplate.yml`, that can be used to sync your repository with this template. By default, this workflow runs at 5:17am every Friday. To change this, edit [this line](https://github.com/jaARke/discord-lambda-py/blob/6712bd3a5e4b2fb69380898bc6b3f756205f4e08/.github/workflows/syncToTemplate.yml#L6). Alternatively, you can manually trigger the workflow by going to "Actions" -> "Sync to Template" -> "Run workflow".

This workflow will automatically merge any template changes without overwriting any custom commands. It will then open a pull request with the changes. Afterwards, you can review the changes and merge them into your repository.

## Usage
1. Go to the "OAuth2" tab in your Discord application's settings.
2. Under "OAuth2 URL Generator", select the "applications.commands" scope.
3. Copy the generated URL and paste it into your browser. This will prompt you to add the bot to a server.
4. Select the server you wish to add the bot to and click "Authorize".
5. Navigate to the server and type `/` in the message box. You should see a list of commands registered to your application.

## Class Reference
### CommandRegistry

The `CommandRegistry` class is responsible for managing commands within an application. It provides functionality to register, update, and find commands. This documentation will cover the class attributes and member functions, along with their respective parameters.

A single `CommandRegistry` object is created when the Lambda function is deployed. During initialization, this object syncs your commands with Discord. It is then serialized and stored in a Lambda layer to be used by the deployed function. This allows the function to access the `CommandRegistry` object without having to reinitialize it on every invocation.

#### Class Attributes

- `commands`: A dictionary storing the registered commands.

#### Constructor

```python
__init__(self, command_dir: str, app_id: str, bot_token: str) -> None
```

The constructor initializes an instance of the `CommandRegistry` class.

- `command_dir`: A string representing the directory where command files are located.
- `app_id`: A string representing the ID of the application associated with the commands.
- `bot_token`: A string representing the token for the bot account.

#### Member Functions

```python
__register_commands(self, command_dir: str) -> None
```

This private method registers commands by loading command files from the specified directory.

- `command_dir`: A string representing the directory where command files are located.

Throws an `Exception` if there is an error loading a command file.

```python
__update_commands(self, app_id: str, bot_token: str) -> None
```

This private method updates the application commands with the Discord API.

- `app_id`: A string representing the ID of the application associated with the commands.
- `bot_token`: A string representing the token for the bot account.

Throws and `Exception` if there is an error updating the application commands.

```python
register_cmd_group(self, name: str, desc: str = None, parent_group: str = None) -> None
```

This method registers a command group.

- `name`: A string representing the name of the command group.
- `desc`: A string representing the description of the command group. Default is `None`.
- `parent_group`: A string representing the name of the parent command group. Default is `None` for top-level command groups.

Throws a `KeyError` if the parent command group does not exist.

```python
register_cmd(self, func: callable, name: str, desc: str = None, cmd_group: str = None, sub_cmd_group: str = None, options: list[CommandArg] = None) -> None
```

This method registers a command.

- `func`: A callable representing the function to be executed for the command.
- `name`: A string representing the name of the command.
- `desc`: A string representing the description of the command. Default is `None`.
- `cmd_group`: A string representing the name of the parent command group. Default is `None` for top-level commands.
- `sub_cmd_group`: A string representing the name of the parent subcommand group. Default is `None`.
- `options`: A list of `CommandArg` objects representing the command options. Default is `None`.

Throws an `Exception` if the subcommand group is registered without a parent command group.

```python
find_func(self, d: dict) -> tuple[callable, dict]
```

This method finds the function associated with a given command.

- `d`: A dictionary representing the command.

Returns:
- A tuple containing the callable function and a dictionary of command arguments.

Throws a `KeyError` if the command is not found and an `AssertionError` if the command function is not callable.

### Interaction
The `Interaction` class is responsible for parsing and storing interaction data and provides member functions to respond to these interactions. This documentation will explain the purpose of each class attribute and member function, along with their respective parameters.

#### Class Attributes

- `type`: A string representing the type of interaction.
- `token`: A string representing the token associated with the interaction.
- `id`: A string representing the ID of the interaction.
- `data`: A dictionary containing additional data associated with the interaction.
- `callback_url`: A string representing the URL for sending callbacks related to the interaction.
- `webhook_url`: A string representing the URL for sending webhooks related to the interaction.
- `timestamp`: A float representing the timestamp when the `Interaction` object was created.

#### Constructor

```python
__init__(self, interaction: dict, app_id: str) -> None
```

The constructor method initializes an instance of the `Interaction` class.

- `interaction`: A dictionary containing the interaction data.
- `app_id`: A string representing the ID of the application associated with the interaction.

#### Member Functions

```python
ping_response(self) -> None
```

This method responds to a ping interaction from the Discord API. Such interactions are used by Discord to verify that the bot is responding to interactions.

```python
defer(self) -> None
```

This method defers the interaction so that a response can be sent later. After an interaction is deferred, a response will need to be sent within 15 minutes to avoid timeout.

```python
__create_channel_message(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> dict
```

This private method creates a dictionary representing a channel message that can be sent as a response or follow-up.

- `content`: A string representing the text content of the message. Default is `None`.
- `embeds`: A list of `Embedding` objects representing embedded content in the message. Default is `None`.
- `ephemeral`: A boolean indicating whether the message should be ephemeral (visible only to the user who triggered the interaction). Default is `True`.

Returns:
- `response`: A dictionary representing the channel message.

```python
send_response(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None
```

This method sends a response to the interaction by updating the original message.

- `content`: A string representing the text content of the response message. Default is `None`.
- `embeds`: A list of `Embedding` objects representing embedded content in the response message. Default is `None`.
- `ephemeral`: A boolean indicating whether the response should be ephemeral (visible only to the user who triggered the interaction). Default is `True`.

```python
send_followup(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None
```

This method sends a follow-up message as a response to the interaction.

- `content`: A string representing the text content of the follow-up message. Default is `None`.
- `embeds`: A list of `Embedding` objects representing embedded content in the follow-up message. Default is `None`.
- `ephemeral`: A boolean indicating whether the follow-up message should be ephemeral (visible only to the user who triggered the interaction). Default is `True`.

### Embedding
The `Embedding` class is responsible for parsing and storing embedded content data and provides member functions to add fields to the embedded content. This documentation will explain the purpose of each class attribute and member function, along with their respective parameters.

#### Class Attributes

- `title`: A string representing the title of the embedding.
- `desc`: A string representing the description of the embedding.
- `url`: A string representing the URL associated with the embedding.
- `color`: An integer representing the color code of the embedding.
- `fields`: A list of dictionaries representing the fields of the embedding.
- `footer`: A dictionary representing the footer of the embedding. Structure is as follows:
    - `text`: A string representing the text to be displayed in the footer.
    - `icon_url`: A string representing the URL of the icon to be displayed in the footer.

#### Constructor

```python
__init__(self, title: str = "", desc: str = "", url: str = "", color: int = "", fields: list[dict] = [], footer: dict = {})
```

The constructor method initializes an instance of the `Embedding` class.

- `title`: A string representing the title of the embedding. Default is an empty string.
- `desc`: A string representing the description of the embedding. Default is an empty string.
- `url`: A string representing the URL associated with the embedding. Default is an empty string.
- `color`: An integer representing the color code of the embedding. Default is an empty integer.
- `fields`: A list of dictionaries representing the fields of the embedding. Default is an empty list.
- `footer`: A dictionary representing the footer of the embedding. See above for the expected structure. Default is an empty dictionary.

#### Member Functions

```python
to_dict(self) -> dict
```

This method converts the `Embedding` object into a dictionary format that can be easily serialized.

Returns:
- `dict`: A dictionary representation of the `Embedding` object.

```python
set_title(self, title: str) -> None
```

This method sets the title of the embedding.

- `title`: A string representing the title to be set for the embedding.

```python
set_description(self, desc: str) -> None
```

This method sets the description of the embedding.

- `desc`: A string representing the description to be set for the embedding.

```python
set_url(self, url: str) -> None
```

This method sets the URL associated with the embedding.

- `url`: A string representing the URL to be set for the embedding.

```python
set_color(self, color: int) -> None
```

This method sets the color code of the embedding.

- `color`: An integer representing the color code to be set for the embedding.

```python
add_field(self, name: str, value: str, inline: bool) -> None
```

This method adds a field to the embedding.

- `name`: A string representing the name of the field.
- `value`: A string representing the value of the field.
- `inline`: A boolean indicating whether the field should be displayed inline or not.

```python
set_footer(self, text: str, icon_url: str = None) -> None
```

This method sets the footer of the embedding.

- `text`: A string representing the text to be set for the footer.
- `icon_url`: A string representing the URL of the icon to be displayed in the footer. Default is `None`.

### CommandArg

The `CommandArg` class represents a command argument that can be used within a command. It provides functionality to define the name, description, type, required flag, and choices for the argument. This documentation will cover the class attributes and member functions, along with their respective parameters.

#### Class Attributes

- **Choice:** The `Choice` class represents a choice option for the command argument.
- **Types:** The `Types` class contains predefined constants representing different types of command arguments.

#### Constructor

```python
__init__(self, name: str, desc: str, type: int, required: bool = True, choices: list[Choice] = None) -> None
```

The constructor initializes an instance of the `CommandArg` class.

- `name`: A string representing the name of the command argument.
- `desc`: A string representing the description of the command argument.
- `type`: An integer representing the type of the command argument.
- `required`: A boolean indicating whether the command argument is required. Default is `True`.
- `choices`: A list of `Choice` objects representing the choices for the command argument. Default is `None`.

#### Member Functions

```python
to_dict(self) -> dict
```

This method converts the `CommandArg` object into a dictionary format that can be easily serialized.

Returns:
- `dict`: A dictionary representation of the `CommandArg` object.
