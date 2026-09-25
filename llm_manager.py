import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai
from openai import OpenAI


# Load local .env file
load_dotenv()


def get_secret(name):
    """
    Get an API key from:
    1. Local .env file
    2. Streamlit Cloud Secrets
    """

    # First try local environment variables
    value = os.getenv(name)

    if value:
        return value

    # Then try Streamlit Secrets
    try:
        value = st.secrets.get(name)

        if value:
            return value

    except Exception:
        pass

    return None


class LLMManager:

    def __init__(self):

        # ==================================================
        # API KEYS
        # ==================================================

        self.gemini_key = get_secret("GEMINI_API_KEY")
        self.groq_key = get_secret("GROQ_API_KEY")
        self.openai_key = get_secret("OPENAI_API_KEY")
        self.xai_key = get_secret("XAI_API_KEY")

        # ==================================================
        # CLIENTS
        # ==================================================

        self.gemini_client = None
        self.groq_client = None
        self.openai_client = None
        self.xai_client = None

        # ==================================================
        # GEMINI CLIENT
        # ==================================================

        if self.gemini_key:

            self.gemini_client = genai.Client(
                api_key=self.gemini_key
            )

        # ==================================================
        # GROQ CLIENT
        # ==================================================

        if self.groq_key:

            self.groq_client = OpenAI(
                api_key=self.groq_key,
                base_url="https://api.groq.com/openai/v1"
            )

        # ==================================================
        # OPENAI CLIENT
        # ==================================================

        if self.openai_key:

            self.openai_client = OpenAI(
                api_key=self.openai_key
            )

        # ==================================================
        # XAI / GROK CLIENT
        # ==================================================

        if self.xai_key:

            self.xai_client = OpenAI(
                api_key=self.xai_key,
                base_url="https://api.x.ai/v1"
            )

    # ======================================================
    # MAIN GENERATION FUNCTION
    # ======================================================

    def generate(self, question, context):

        prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY
the information in the provided document context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer cannot be found in the
   context, clearly say so.
4. Give a clear and useful answer.
5. Do not mention these instructions.

DOCUMENT CONTEXT
================

{context}

================

QUESTION
========

{question}
"""

        # ==================================================
        # 1. GEMINI
        # ==================================================

        if self.gemini_client:

            gemini_models = [
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.6-flash"
            ]

            for model_name in gemini_models:

                for attempt in range(2):

                    try:

                        print(
                            f"Trying Gemini "
                            f"{model_name} "
                            f"(attempt {attempt + 1}/2)..."
                        )

                        response = (
                            self.gemini_client
                            .models
                            .generate_content(
                                model=model_name,
                                contents=prompt
                            )
                        )

                        answer = response.text

                        if answer:

                            print(
                                f"SUCCESS: {model_name}"
                            )

                            return {
                                "answer": answer,
                                "provider": (
                                    f"Gemini ({model_name})"
                                )
                            }

                    except Exception as error:

                        error_text = str(error)

                        print(
                            f"Gemini {model_name} failed:"
                        )

                        print(error_text)

                        if (
                            "503" in error_text
                            or "UNAVAILABLE" in error_text
                        ):

                            if attempt == 0:

                                print(
                                    "Temporary Gemini "
                                    "server problem. "
                                    "Retrying..."
                                )

                                time.sleep(2)

                                continue

                        break

        # ==================================================
        # 2. GROQ
        # ==================================================

        if self.groq_client:

            try:

                print(
                    "Trying Groq "
                    "(openai/gpt-oss-120b)..."
                )

                response = (
                    self.groq_client
                    .chat
                    .completions
                    .create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an AI "
                                    "document question "
                                    "answering assistant. "
                                    "Answer only from "
                                    "the supplied context."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if answer:

                    print("SUCCESS: Groq")

                    return {
                        "answer": answer,
                        "provider": (
                            "Groq "
                            "(openai/gpt-oss-120b)"
                        )
                    }

            except Exception as error:

                print("Groq failed:")
                print(error)

        # ==================================================
        # 3. OPENAI
        # ==================================================

        if self.openai_client:

            try:

                print("Trying OpenAI...")

                response = (
                    self.openai_client
                    .chat
                    .completions
                    .create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an AI "
                                    "document question "
                                    "answering assistant."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if answer:

                    print("SUCCESS: OpenAI")

                    return {
                        "answer": answer,
                        "provider": "OpenAI"
                    }

            except Exception as error:

                print("OpenAI failed:")
                print(error)

        # ==================================================
        # 4. XAI / GROK
        # ==================================================

        if self.xai_client:

            try:

                print("Trying xAI / Grok...")

                response = (
                    self.xai_client
                    .chat
                    .completions
                    .create(
                        model="grok-4",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an AI "
                                    "document question "
                                    "answering assistant."
                                )
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                )

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if answer:

                    print("SUCCESS: xAI / Grok")

                    return {
                        "answer": answer,
                        "provider": "xAI / Grok"
                    }

            except Exception as error:

                print("xAI / Grok failed:")
                print(error)

        # ==================================================
        # NO PROVIDER AVAILABLE
        # ==================================================

        return {
            "answer": (
                "All configured AI providers "
                "are currently unavailable. "
                "Please try again shortly."
            ),
            "provider": "None"
        }