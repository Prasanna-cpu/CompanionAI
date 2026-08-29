from langchain_core.prompts import prompt

from .llms import get_openai_llm
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor

from .tools import send_me_email, get_unread_emails, research_email


def get_weather(city : str) -> str:
    return f"It is sunny in {city}"


EMAIL_TOOLS = {
    "send_me_email" : send_me_email,
    "get_unread_emails" : get_unread_emails,
    "research_email" : research_email
}

EMAIL_TOOLS_LIST = [send_me_email, get_unread_emails, research_email]


def get_email_agent():
    model = get_openai_llm()
    model = model.bind_tools(EMAIL_TOOLS_LIST)
    agent = create_agent(
        model = model,
        tools = EMAIL_TOOLS_LIST,
        system_prompt = "You are a helpful assistant for managing my email inbox for generating, sending, and reviewing emails.",
        name="email_agent"
    )

    return agent

def get_research_agent():
    model = get_openai_llm()
    agent = create_agent(
        model = model,
        tools = [research_email],
        system_prompt = "You are a helpful research assistant for preparing email data.",
        name="research_agent"
    )
    return agent

def get_supervisor():
    llm = get_openai_llm()
    supervisor = create_supervisor(
        agents=[get_email_agent(), get_research_agent()],
        model=llm,
        prompt=(
            "You manage a research assistant and a email inbox manager assistant . Assign work to them"
        )
    ).compile()
    return supervisor


# supervisor = get_supervisor()
# result = supervisor.invoke({"messages" : [{
#     "role" : "user",
#     "content" : "Find out how to create a latte and then email it"
# }]})
# print(result)

# agent = get_email_agent()
# result = agent.invoke({"messages" : "Send me an Email about Tea in 60 words"})
# print(result)

