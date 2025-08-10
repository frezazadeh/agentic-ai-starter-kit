# Agentic AI Starter Kit

A **from-scratch** and **professional** example of building a minimal **Agentic AI** in Python.

This project demonstrates how to create an AI agent that:
1. **Plans** — proposes a challenging question.
2. **Acts** — calls external tools via OpenAI's function calling.
3. **Reflects** — delivers a concise, checked answer.

It’s designed for **educational purposes** and as a **starter template** for more complex agent systems.

---

## 🚀 Features
- **Clean, modular structure** for scalability.
- **Secure API key handling** with `.env`.
- **Tool registry** for adding new capabilities easily.
- **Function calling** to integrate Python functions with AI reasoning.
- **Lightweight memory buffer** for conversation context.
- Optional **reflection step** to sanity-check answers.

---

## 📂 Project Structure
```
agentic-ai-starter/
├─ .env.example          # Environment variable template
├─ pyproject.toml        # Dependencies & settings
├─ README.md             # Project documentation
├─ src/
│  ├─ config.py          # Environment loading & client factory
│  ├─ tools/
│  │  ├─ __init__.py
│  │  └─ math_tool.py    # Example tool: safe math evaluator
│  ├─ agent/
│  │  ├─ __init__.py
│  │  └─ core.py         # Agent orchestration logic
│  └─ run_demo.py        # Demo script
```

---

## 🛠 Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/agentic-ai-starter-kit.git
cd agentic-ai-starter-kit
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -U pip
pip install -e .
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in:
```
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4.1
OPENAI_FAST_MODEL=gpt-4.1-mini
OPENAI_TINY_MODEL=gpt-4.1-nano
```

---

## ▶️ Usage
```bash
python -m src.run_demo
```

Example output:
```
Phase 1: Propose a challenging question
Question: If you triple a number and then subtract 14, you get 25. What is the number?

Phase 2: Solve with tools if needed
Answer: The number is 13.
```

---

## 📚 How It Works
- **`Agent` class** orchestrates planning, acting, and reflecting.
- **Tools** are registered with JSON schema definitions so the model knows how to call them.
- **Function calling** lets the model trigger Python functions mid-conversation.
- **Memory buffer** maintains recent messages.

---

## 🧩 Extending the Agent
1. Create a new tool in `src/tools/`.
2. Define its parameters and handler.
3. Register it in `Agent.__init__()`.
4. Update prompts to encourage tool use.

---

## 📄 License
MIT License — free to use and modify for personal or commercial projects.

---

## 📌 References
- [OpenAI Python SDK Docs](https://platform.openai.com/docs/)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Model List](https://platform.openai.com/docs/models)
