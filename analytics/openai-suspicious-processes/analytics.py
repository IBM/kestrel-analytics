#!/usr/bin/env python3

import os
import pandas as pd

from openai import OpenAI


OPENAI_MODEL = "gpt-3.5-turbo"

PROMPT = """
    The following dataframe contains information about different processes running on a system: {}. 
    Rank those processes by suspicioussness and give an explanation for the top 10.
    """

client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def analytics(df):
    """
    Given a prompt and process information in the dataframe,
    rank the processes by suspiciousness and give an explanation
    for the top 10 suspicious processes.
    """

    complete_prompt = PROMPT.format(df.to_json())
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": complete_prompt,
            }
        ],
        model=OPENAI_MODEL,
    )

    display = (
                f"<p><b>Prompt:</b> {PROMPT.format(df)} </p>"
                f"<p><b>Answer:</b> {chat_completion.choices[0].message.content}</p>"
              )

    return df, display
