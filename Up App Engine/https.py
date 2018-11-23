from flask import Flask
app = Flask(__name__)



@app.route('/.well-known/acme-challenge/WgOUkQlAmk4TobLBW3j15IDccgf4ySvDj4BjtiwR3lo')
def hello():
    return "WgOUkQlAmk4TobLBW3j15IDccgf4ySvDj4BjtiwR3lo.MobMwZzQLfOlWDWet5Xo0_SkeGcVeTknpn0c8Eq6Z9s"

@app.route('/.well-known/acme-challenge/2EG8uQoGxzyENS86g4xPkjceFuY-T66qOpGAWqBiNlI')
def hello2():
    return "2EG8uQoGxzyENS86g4xPkjceFuY-T66qOpGAWqBiNlI.MobMwZzQLfOlWDWet5Xo0_SkeGcVeTknpn0c8Eq6Z9s"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
