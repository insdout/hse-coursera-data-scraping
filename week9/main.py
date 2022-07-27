from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import io
import base64
import matplotlib
import numpy as np
import json
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def find_roots(a, b, c):
    a = int(a)
    b = int(b)
    c = int(c)
    D = int(b) ** 2 - 4 * int(a) * int(c)
    if a == b == c == 0:
        return [float("inf")]
    elif a == b == 0:
        return []
    elif a == 0:
        return [-c/b]
    elif D < 0:
        return []
    elif D == 0:
        return [-b / (2 * a)]
    else:
        return [(-b - np.sqrt(D)) / (2 * a), (-b + np.sqrt(D)) / (2 * a)]


def func(a, b, c, x):
    a = int(a)
    b = int(b)
    c = int(c)
    return a*x**2 + b*x + c


@app.get("/")
async def root(request: Request, message='Hello, Coursera students'):
    # return {"message": "Hello World"}
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "message": message})


@app.get("/solve")
async def solve(request: Request, a, b, c):
    return json.JSONEncoder(allow_nan=True).encode(find_roots(a, b, c))
    # return {"roots": find_roots(a, b, c)}


@app.post("/main")
async def show_plot(request: Request,
                    a: str = Form(...),
                    b: str = Form(...),
                    c: str = Form(...)):

    roots = find_roots(a, b, c)

    if not roots or roots[0] == float("inf"):
        if int(a) != 0:
            left = -int(b)/(2*int(a)) - 10
            right = -int(b)/(2*int(a)) + 10
        else:
            left = - 10
            right = 10
    elif len(roots) == 1:
        left = roots[0] - 10
        right = roots[0] + 10
    else:
        left = min(roots) - 10
        right = max(roots) + 10

    x = np.linspace(left, right, 100)
    y = func(a, b, c, x)
    zero = np.zeros_like(x)

    with plt.rc_context(
            {'axes.edgecolor': (0.84, 0.6, 0.13),
             'xtick.color': (0.84, 0.6, 0.13),
             'ytick.color': (0.84, 0.6, 0.13),
             'figure.facecolor': (0.16, 0.16, 0.16)}
    ):
        fig = plt.figure()
        plt.plot(x, y, color=[0.84, 0.6, 0.13])
        plt.plot(x, zero, '--', color=[0.84, 0.6, 0.13])
        if roots and roots[0] != float("inf"):
            plt.scatter(roots,
                        np.zeros_like(roots),
                        s=180,
                        marker="+",
                        color=[0.84, 0.6, 0.13])
        ax = plt.gca()
        ax.set_facecolor((0.16, 0.16, 0.16))
        fig.patch.set_facecolor((0.16, 0.16, 0.16))
        png_image = io.BytesIO()
        fig.savefig(png_image)

    png_image_b64_string\
        = base64.b64encode(png_image.getvalue()).decode('ascii')
    return templates.TemplateResponse("index.html",
                                {"request": request,
                                 "a": a,
                                 "b": b,
                                 "c": c,
                                 "roots": roots,
                                 "picture": png_image_b64_string})

