from app import app

print("Registered routes:")
for route in app.routes:
    print(route.path, route.methods)
