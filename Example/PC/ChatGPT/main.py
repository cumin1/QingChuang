import openai
openai.api_key = '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'

msg = input('请输入问题:')
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": msg}
  ]
)
print(completion.choices[0].message['content'])
