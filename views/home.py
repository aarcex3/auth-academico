from fronty.html import Html,Head,Meta,Title,Body,Link
from fastapi.responses import HTMLResponse
from fronty.html.widgets import FormWidget

def index() -> HTMLResponse:
    return Html(
        Head(
            Title('Academico UPA'),  
            Meta(charset='utf-8'),  
            
            Meta(name='viewport', content='width=device-width, initial-scale=1'),

            # Bootstrap CSS
            Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css',
                 integrity='sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD', crossorigin='anonymous'),
        ),
        login_view(),
        ).render()


def login_view() -> HTMLResponse:
    return Body(
            FormWidget(action="/token",load_css=True,method='post')
        )