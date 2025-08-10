from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from ..config import Settings
from ..tools.math_tool import MathRequest, evaluate_math


ToolFn = Callable[[Dict[str, Any]], str]


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: ToolFn


@dataclass
class Memory:
    """Very lightweight conversational memory buffer."""
    turns: List[Dict[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def as_messages(self) -> List[ChatCompletionMessageParam]:
        return [{"role": t["role"], "content": t["content"]} for t in self.turns]


class Agent:
    """
    A minimal agent that:
    1) Plans a hard question,
    2) Solves it with tool calls if needed,
    3) Reflects with a concise explanation (no chain-of-thought leakage).
    """

    def __init__(self, client: OpenAI, settings: Settings):
        self.client = client
        self.settings = settings
        self.memory = Memory()
        self.tools: Dict[str, ToolSpec] = {}

        self.register_tool(
            ToolSpec(
                name="evaluate_math",
                description="Safely evaluate arithmetic, sqrt, or factorial.",
                parameters={
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"},
                        "mode": {"type": "string", "enum": ["eval", "sqrt", "factorial"]},
                    },
                    "required": ["expression", "mode"],
                },
                handler=lambda args: evaluate_math(args),  # simple adapter
            )
        )

    def register_tool(self, tool: ToolSpec) -> None:
        self.tools[tool.name] = tool

    def propose_question(self) -> str:
        """Use a fast model to generate a challenging, concise question."""
        user_prompt = (
            "Propose one difficult, precise question that tests reasoning ability. "
            "Output only the question text—no preamble or answer."
        )
        resp = self.client.chat.completions.create(
            model=self.settings.model_fast,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
        )
        question = (resp.choices[0].message.content or "").strip()
        self.memory.add("user", f"Question to solve: {question}")
        return question

    def solve(self, question: str) -> str:
        """
        Let a stronger model reason, call tools, and produce a concise final answer.
        We instruct the model to use tools when beneficial and to avoid revealing hidden chain-of-thought.
        """
        sys = (
            "You are a precise problem solver. "
            "Use tools when arithmetic is nontrivial. "
            "Return a final answer with a short explanation, no hidden reasoning steps."
        )

        tool_defs = [
            {
                "type": "function",
                "function": {
                    "name": spec.name,
                    "description": spec.description,
                    "parameters": spec.parameters,
                },
            }
        for spec in self.tools.values()
        ]

        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": sys},
            *self.memory.as_messages(),
            {"role": "user", "content": question},
        ]

        # First pass: allow the model to request a tool call if it wants
        first = self.client.chat.completions.create(
            model=self.settings.model_default,
            messages=messages,
            tools=tool_defs,
            tool_choice="auto",
            temperature=0.2,
        )

        msg = first.choices[0].message

        if msg.tool_calls:
            # Execute each tool call in order and append results to the conversation
            for call in msg.tool_calls:
                name = call.function.name
                args = call.function.arguments  # JSON string (SDK parses for you on some versions)
                # Some SDK versions pass a dict; normalize:
                if isinstance(args, str):
                    import json
                    parsed = json.loads(args)
                else:
                    parsed = args

                result = self.tools[name].handler(parsed)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": name,
                        "content": result,
                    }
                )

            # Second pass: get the final answer using the tool results
            second = self.client.chat.completions.create(
                model=self.settings.model_default,
                messages=messages + [{"role": "assistant", "content": None, "tool_calls": msg.tool_calls}],
                temperature=0.2,
            )
            final = (second.choices[0].message.content or "").strip()
        else:
            # No tools needed—use the assistant’s draft directly
            final = (msg.content or "").strip()

        self.memory.add("assistant", final)
        return final
