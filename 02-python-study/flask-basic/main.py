from flask import Flask
# Flask: Python micro web framework
# - Lightweight and flexible (unlike Django which is full-featured)
# - Similar to Spring Boot but simpler
# - Built on Werkzeug WSGI toolkit
# - Easy to start, can scale up with extensions

#Java
#[browser] ←→ [Apache/Nginx] ←→ [Spring Boot + Tomcat] ←→ [MySQL]
#Python
#[browser] ←→ [Nginx] ←→ [Flask + Gunicorn] ←→ [PostgreSQL]

app = Flask(__name__)  # create Flask instance

@app.route('/')        # @ -> decorator (similar to Java annotation)
def hello():           # def -> function definition (like Java method)
    return 'Hello World!'
# Java Spring equivalent:
# @RequestMapping("/")
# public String hello() {
#     return "Hello World!";
# }

@app.route('/user/<name>')
#@app.route('/api/users', methods=['GET'])
def hello_user(name):  # no type declaration needed (dynamic typing)
    return 'Hello %s!' % name
# Java Spring equivalent:
# @RequestMapping("/user/{name}")  # ${name} → {name}
# public String hello_user(@PathVariable String name){
#     return "Hello " + name + "!";
# }

if __name__ == '__main__':
    # app.run(debug=True)       # simple Werkzeug server run
    app.run(
        host='0.0.0.0',    # Allow access from all IPs
        port=5000,         # Port number
        debug=True         # Auto restart when code changes
    )