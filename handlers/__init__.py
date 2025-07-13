def register_handlers(app):
    from . import commands
    from . import inline
    from . import callback_handlers

    commands.register(app)
    callback_handlers.register_callback(app) 
    inline.register_inline(app)