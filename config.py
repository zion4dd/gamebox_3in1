import sys, os

DEV = False

def get_ico(app):
        try:
            if DEV:
                app.iconbitmap(bitmap=app.icofile)
            else:
                path = os.path.join(sys._MEIPASS, app.icofile)
                app.iconbitmap(bitmap=path)
        except: pass
