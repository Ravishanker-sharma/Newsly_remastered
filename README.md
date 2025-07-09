# 📰 Newsly Remastered — AI-Powered Personalized News Platform

**Newsly Remastered** is a full-stack, LLM-integrated news assistant designed to deliver a personalized, interactive, and intelligent news experience. Inspired by the Headlyne app, this solo-built project combines real-time web scraping, generative AI, vector-based personalization, and natural interaction—all packed into a clean, modular architecture.

---

## 🔍 Features Overview

### 🚀 Core Capabilities (v1.0)
• **Live News Scraping**  
↳ Multi-threaded Python scrapers collect real-time content (headlines, images, articles) from trusted sources.

• **AI-Enhanced News Generation**  
↳ Scraped content is processed using a **Gemini LLM via LangChain** to generate rewritten headlines, bullet points, FAQs, and metadata.

• **Contextual Chatbot on Each News Card**  
↳ Every news item has its own **LLM agent** powered by LangGraph, capable of answering user queries with memory and tool use.

• **Voice Interaction Support**  
↳ Users can send voice messages in `.webm`, which are converted to `.wav` and transcribed using `speech_recognition`.

• **Custom Search Engine Integration**  
↳ When the LLM lacks context, a Yahoo-powered search + fallback web scraper fetches supplemental information (without API costs).

• **Backend + Frontend**  
↳ `FastAPI` for backend processing  
↳ `PostgreSQL` for storing articles and user feedback  
↳ `React + Bolt.AI` for an interactive and modern UI  

---

## 🆕 New Features (v2.0)

### 📌 “For You” Section — Vector-Based Personalized News Feed  
• Calculates user interest using **vector similarity** between past liked/disliked articles  
• Displays a **probability score** showing how likely a user is to engage with a given news item  
• Enables a truly adaptive feed that evolves with user interaction

### 📚 Fully Detailed News View — AI-Powered Contextual Expansion  
• Newsly gathers extra background using live web search  
• A **Gemini LLM** processes the data into a **long-form, context-rich article**  
• Users get a deeper, more nuanced understanding of any story with just one click

---

## 💡 Why Newsly Matters

Newsly is not just a portfolio project—it's a complete demonstration of how to integrate modern AI tools into real-world applications. It shows how LLMs, embeddings, memory, and intelligent scraping can work together to deliver deeply personalized user experiences.

---

## 📎 Links

• 🔗 [LinkedIn Feature Overview Post](https://www.linkedin.com/feed/update/urn:li:activity:7347952350495416322/)  
• 📘 [Medium Technical Walkthrough](https://lnkd.in/gRf3Bmen)  

---

## 🛠 Tech Stack

• **Backend:** FastAPI, PostgreSQL, LangChain, LangGraph  
• **Frontend:** React, Bolt.AI  
• **AI/LLM:** Gemini (via LangChain)  
• **Voice:** `speech_recognition` module  
• **Vector Embeddings:** Used for personalized recommendation  
• **Search & Scraping:** Yahoo Search + Fallback Web Scraper (custom)

---

## 📌 Future Improvements
• Faster Response Times
↳ Optimize LLM pipelines and API latency for real-time interactions, especially during multi-agent operations.

• Multi-Language Support
↳ Add multilingual scraping and LLM output (e.g., Hindi, English) to broaden accessibility and regional relevance.

• Text-to-Speech — News That Speaks
↳ Integrate TTS (Text-to-Speech) functionality to allow users to listen to news content directly.

• News Aggregation from Multiple Sources
↳ Extend current scraping system to handle multiple trusted sources to reduce bias and increase diversity of content.

• UI/UX Enhancements
↳ Refine frontend interface using better layout management, personalized visual cues, and responsive design improvements.

---

## 🤝 Contributions

This is a solo-built project, but contributions are welcome. Feel free to fork the repo or raise issues if you’d like to help improve Newsly.

---




