from .app import app
from .error_handlers import register_error_handlers
from .middleware import register_middleware
from .views.routers import router

# Initialize the app with all components
register_error_handlers(app)
register_middleware(app)

# Include routers
app.include_router(router)
