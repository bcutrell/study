import responder
import time

# Running through DOC examples

api = responder.API()

@api.route("/greeting/{greeting}")
async def greet_world(req, resp, *, greeting):
  resp.text = f"{greeting}, world!"


@api.route("/incoming")
async def receive_incoming(req, resp):

  @api.background.task
  def process_data(data):
    """Just sleeps for three seconds, as a demo."""
    time.sleep(3)
    print("Done")

  # Parse the incoming data as form-encoded.
  # Note: 'json' and 'yaml' formats are also automatically supported.
  data = await req.media()

  # Process the data (in the background).
  process_data(data)

  # Immediately respond that upload was successful.
  resp.media = {'success': True}

@api.route("/hello/{who}/html")
def hello_html(req, resp, *, who):
  resp.content = api.template('hello.html', who=who)

if __name__ == '__main__':
  api.run()
