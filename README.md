
# 🪳 Chitin.ai — Indestructible Agentic Memory

> **Autonomous Infrastructure Remediation Engine powered by CockroachDB Distributed Vector Search, Managed MCP, and AWS Bedrock.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-CockroachDB_Cloud-ff69b4.svg)](https://www.cockroachlabs.cloud/)
[![Cloud](https://img.shields.io/badge/Cloud-AWS_Bedrock_%2B_Lambda-FF9900.svg)](https://aws.amazon.com/)

---

## 📌 Problem Statement

When an autonomous AI agent manages production cloud infrastructure, loss of context isn't an inconvenience—it's a critical outage. Traditional databases were built for human-scale interactions, but autonomous agentic swarms spawn dynamically, write state constantly, and execute complex workflows across distributed regions. 

If an agent crashes mid-remediation or suffers a network partition, a typical in-memory or single-region vector store loses context. The agent either halts or hallucinates destructive commands based on fragmented memory. **Chitin.ai** provides autonomous infrastructure remediation agents with an unbreakable, persistent memory layer powered by **CockroachDB** and **AWS**.

---

## 🏗️ System Architecture

```text
                  ┌─────────────────────────────────────────┐
                  │          AWS EventBridge / Logs         │
                  └────────────────────┬────────────────────┘
                                       │ (Incident Trigger)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │    AWS Lambda + Amazon Bedrock Agent    │
                  └───────┬─────────────────┬───────────────┘
                          │                 │
         (1. Read State & │                 │ (2. Vector Search
          Inspect Health) │                 │    Post-mortems)
                          ▼                 ▼
 ┌───────────────────────────────────┐   ┌───────────────────────────────────┐
 │   CockroachDB Managed MCP Server  │   │ CockroachDB Vector Index Engine   │
 └───────────────────────────────────┘   └───────────────────────────────────┘
                          │                 │
                          └────────┬────────┘
                                   │ (3. Select Action Plan)
                                   ▼
                  ┌─────────────────────────────────────────┐
                  │    CockroachDB Agent Skills Execution   │
                  └────────────────────┬────────────────────┘
                                       │ (4. Execute Infra Fix)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │      Agent-Ready ccloud CLI / AWS       │
                  └─────────────────────────────────────────┘
