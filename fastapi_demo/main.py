from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, BackgroundTasks
import openai
import os
import sys
from langfuse import Langfuse
from langfuse.model import CreateGeneration, CreateScore, CreateTrace, CreateSpan
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Operation on startup

    yield  # wait until shutdown

    # Flush all events to be sent to Langfuse on shutdown. This operation is blocking.
    langfuse.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def main_route():
    return {"message": "Hey, It is me Goku from the future."}


langfuse = Langfuse("pk-lf-1234567890", "sk-lf-1234567890", "http://localhost:3000")


async def get_response_openai(prompt, background_tasks: BackgroundTasks):
    try:
        trace = langfuse.trace(
            CreateTrace(
                name="lilly-this-is-so-great-new-blub",
                user_id="test",
                metadata="test",
            )
        )

        trace = trace.score(
            CreateScore(
                name="user-explicit-feedback",
                value=1,
                comment="I like how personalized the response is",
            )
        )

        generation = trace.generation(
            CreateGeneration(name="his-is-so-great-new", metadata="test")
        )

        sub_generation = generation.generation(
            CreateGeneration(name="yet another child", metadata="test")
        )

        sub_sub_span = sub_generation.span(
            CreateSpan(name="sub-sub-sub-span", metadata="test")
        )

        sub_sub_span = sub_sub_span.score(
            CreateScore(
                name="user-explicit-feedback-o",
                value=1,
                comment="I like how personalized the response is",
            )
        )

        response = {"status": "success", "message": "this is a test message"}
    except Exception as e:
        print("Error in creating campaigns from openAI:", str(e))
        return 503
    return response


@app.get(
    "/campaign/",
    tags=["APIs"],
)
async def campaign(
    background_tasks: BackgroundTasks, prompt: str = Query(..., max_length=20)
):
    return await get_response_openai(prompt, background_tasks)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("fastapi_demo.main:app", host="0.0.0.0", port=8000, reload=True)
