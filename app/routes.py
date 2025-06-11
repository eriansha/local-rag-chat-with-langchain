from flask import Blueprint, request, Response, stream_with_context
from app.rag_engine import get_qa_chain
from app.utils import StreamHandler

routes = Blueprint('routes', __name__)

@routes.route("/ask", methods=["POST"])
def ask_question():
  question = request.json.get("question")
  handler = StreamHandler()

  qa_chain = get_qa_chain(handler)
  _ = qa_chain.invoke(question)  # triggers generation, streams tokens via callback

  # strea_with_context need pass generator
  def generate():
    for token in handler.get_tokens():
      yield token

  return Response(stream_with_context(generate()), mimetype="text/event-stream")
