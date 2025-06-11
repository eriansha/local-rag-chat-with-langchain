from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
  def __init__(self):
    self.queue = []

  def on_llm_new_token(self, token: str, **kwargs):
    self.queue.append(token)

  def get_tokens(self):
    while self.queue:
      yield self.queue.pop(0)
