import argparse
import os, sys, json
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

SYSTEM_PROMPT_DEFAULT = "根据下面提供的上下文用中文回答问题: \n{}"
SYSTEM_PROMPT_REPO = "下面是一个代码仓库中的代码，根据代码回答我的问题: \n{}"

SYSTEM_PROMPT = {
    "repo": SYSTEM_PROMPT_REPO,
    "default": SYSTEM_PROMPT_DEFAULT,
}

parser = argparse.ArgumentParser(description="llm")
parser.add_argument("--prompt", default="")
parser.add_argument("--sys_prompt", default="default", choices=["repo", "default"])
parser.add_argument("--context", required=False)
parser.add_argument("--pipe", action="store_true")
parser.add_argument("--chat", action="store_true")
parser.add_argument("--markdown", action="store_true")
args = parser.parse_args()
prompt = args.prompt


def gemini(
    q, context, use_chat=False, markdown=False, sys_prompt=SYSTEM_PROMPT_DEFAULT
):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    api_key = os.getenv("GEMINI_KEY", "")
    genai.configure(api_key=api_key)
    os.environ["https_proxy"] = os.getenv("PROXY", "")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    if context:
        prompt = sys_prompt.format(context)
    else:
        prompt = f"{q}"
    if markdown:
        use_stream = False
    else:
        use_stream = True
    if use_chat:
        history = [
            {"role": "user", "parts": prompt},
            {
                "role": "model",
                "parts": "Great to meet you. What would you like to know?",
            },
        ]
        chat = model.start_chat(history=history)
        while True:
            i = input(" > ")
            if i in (".exit", ".q", "q", "exit"):
                break
            response = chat.send_message(
                i, stream=use_stream, safety_settings=safety_settings
            )
            if use_stream:
                for chunk in response:
                    print(chunk.text)
            else:
                console = Console()
                markdown = Markdown(response.text)
                console.print(markdown)
    else:
        response = model.generate_content(
            prompt, stream=use_stream, safety_settings=safety_settings
        )
        if use_stream:
            for chunk in response:
                print(chunk.text)
        else:
            console = Console()
            markdown = Markdown(response.text)
            console.print(markdown)


def process_input():
    context = None
    if args.context:
        if os.path.isdir(args.context):
            context = ""
            for root, dirs, files in os.walk(args.context):
                for file in files:
                    fullpath = os.path.join(root, file)
                    if fullpath.endswith(".py") and "venv" not in fullpath:
                        print("add to context: ", fullpath)
                        with open(fullpath, encoding="utf8") as f:
                            content = f.read()
                            context += f"=== {fullpath} === \n\n{content}\n\n"
        else:
            with open(args.context, encoding="utf8") as f:
                context = f.read()
    elif args.pipe:
        context = sys.stdin.read()
    gemini(
        prompt,
        context,
        use_chat=args.chat,
        markdown=args.markdown,
        sys_prompt=SYSTEM_PROMPT.get(args.sys_prompt, SYSTEM_PROMPT_DEFAULT),
    )


if __name__ == "__main__":
    process_input()
