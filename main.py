from datetime import datetime
from fastapi import FastAPI, Query, BackgroundTasks
import openai
import os
import sys
from langfuse import LangfuseAsync
from langfuse.api.model import (
    CreateGeneration,
    CreateScore,
    CreateSpan,
    CreateTrace,
)

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...")
if not len(OPENAI_API_KEY):
    print("Please set OPENAI_API_KEY environment variable. Exiting.")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY


@app.get("/")
async def main_route():
    return {"message": "Hey, It is me Goku"}


langfuse = LangfuseAsync(
    "pk-lf-1234567890", "sk-lf-1234567890", "http://localhost:3000"
)


async def get_response_openai(prompt, background_tasks: BackgroundTasks):
    try:
        trace = await langfuse.trace(
            CreateTrace(
                name="lilly-this-is-so-great-new",
                user_id="test",
                metadata="test",
            )
        )

        trace = await trace.score(
            CreateScore(
                name="user-explicit-feedback",
                value=1,
                comment="I like how personalized the response is",
            )
        )

        generation = await trace.generation(
            CreateGeneration(name="his-is-so-great-new", metadata="test")
        )

        sub_generation = await generation.generation(
            CreateGeneration(name="yet another child", metadata="test")
        )

        sub_sub_span = await sub_generation.span(
            CreateSpan(name="sub-sub-sub-span", metadata="test")
        )

        sub_sub_span = await sub_sub_span.score(
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


async def flush(langfuse: LangfuseAsync):
    print("flushing")
    await langfuse.flush()
    print("flushed")


@app.get(
    "/campaign/",
    tags=["APIs"],
)
async def campaign(
    background_tasks: BackgroundTasks, prompt: str = Query(..., max_length=20)
):
    return await get_response_openai(prompt, background_tasks)
