# DEFEND the MCP

Welcome to Phase 3 of the workshop! In this phase we will **threat model** a multi-agent customer support system built on MCP. You will work in **groups** to identify threats, trust boundaries, and mitigations using the architecture and materials in this folder.

---

## Hands-on exercise

We will **break into groups** and threat model the application described below. Apply what you learned about threat modeling to this architecture: identify threats, trust-boundary risks, and mitigations.

---

## Architecture (reference)

The system is a **multi-agent customer support platform**: an AI orchestrator talks to three MCP servers (Customer Data, Knowledge Base, Internal Systems), which in turn connect to databases and backend APIs. 

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent Orchestrator                    │
│                    (Claude/GPT-4 based system)                  │
│  • Manages conversation context                                 │
│  • Invokes MCP tools                                            │
│  • Combines responses                                           │
└──────────────┬─────────────┬─────────────┬──────────────────────┘
               │             │             │
       ┌───────▼──────┐  ┌──▼───────────┐  ┌▼────────────────────┐
       │   Customer   │  │   Knowledge  │  │  Internal Systems   │
       │   Data MCP   │  │   Base MCP   │  │      MCP Server     │
       │   Server     │  │   Server     │  │                     │
       └──────┬───────┘  └──┬───────────┘  └─┬───────────────────┘
              │             │                 │
     ┌────────┴─────────┐   │        ┌────────┴──────────┐
     │                  │   │        │                   │
┌────▼─────┐    ┌──────▼───▼─────┐   │   ┌───────────┐   │
│ Customer │    │  Vector Store  │   │   │  Billing  │   │
│ Database │    │  (Embeddings)  │   │   │  System   │   │
│  (SQL)   │    │                │   │   │  (API)    │   │
└──────────┘    └────────────────┘   │   └───────────┘   │
                                     │                   │
                                     │   ┌───────────┐   │
                                     │   │ Ticketing │   │
                                     │   │  System   │   │
                                     │   │  (API)    │   │
                                     │   └───────────┘   │
                                     └───────────────────┘
```

---
