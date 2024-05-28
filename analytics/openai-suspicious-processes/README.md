# OpenAI suspicious processes ranking

## Goal

Analyze a list of potentially suspicious processes by prompting an OpenAI model.

## Usage

The example `PROMPT` in this analytic asks ChatGPT (`gpt-3.5-turbo` version) to rank the processes provided in the input dataframe and
to give explanations for the top 10 suspicious processes.

## Example

Assume you have a variable `procs` with `process` entities. You can prompt the model to rank the processes with the following command:

```
APPLY python://openai-suspicious-processes ON procs
```

The `OPENAI_API_KEY` variable must be provided in the huntbook environment.
