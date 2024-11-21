from openai import OpenAI

from src.config import BotConfig

client = OpenAI(api_key=BotConfig.gpt_token, )


async def gpt_api_func(prompt, style):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system"},
                  {
                      "role": "user",
                      "content": [
                          {"type": "text", "text": prompt.replace('STYLE', style)},

                      ],
                  },
                  ],
        temperature=0
    )
    return response
