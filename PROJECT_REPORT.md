# ShopMate AI E-Commerce Customer Support Agent

## 1. Project Overview

### Project Title

**ShopMate AI - E-Commerce Customer Support Agent**

### Problem Statement

Online shoppers often need quick help with product discovery, recommendations, order tracking, and return policies. Traditional support systems may require manual intervention or force customers to search through several pages before finding an answer. This project addresses that problem with a conversational AI assistant that provides store support through a single web interface.

### Brief Description

ShopMate AI is a web-based e-commerce demonstration application. Customers can browse products, search by category or price, add items to a bag, manage a wishlist, track demo orders, and chat with an AI shopping assistant. The assistant uses a locally hosted Ollama language model and controlled application tools to answer questions using the product catalog, order data, and return policy.

The application includes two compatible backend implementations:

- A Node.js and Express server on port 3000.
- A FastAPI and Python server on port 8000.

Both backends serve the same frontend experience and provide an offline fallback when Ollama is unavailable.

## 2. Objectives and Proposed Solution

### Project Objectives

1. Build a responsive and accessible e-commerce storefront.
2. Provide conversational product discovery and shopping guidance.
3. Support order-status lookup using known order identifiers.
4. Provide recommendations based on category, interest, and budget.
5. Explain the demo return and refund policy clearly.
6. Demonstrate local AI integration without depending on a paid cloud model.
7. Keep the design ready for replacement of demo data with database or API services.

### How the Agentic AI Solution Works

The assistant follows a tool-calling workflow:

1. The customer submits a message from the AI Stylist page.
2. The backend sends the conversation and catalog context to Ollama.
3. Ollama decides whether the request needs an application tool.
4. The backend validates the requested action and executes the matching tool.
5. The tool result is sent back to Ollama for a natural-language response.
6. The response is displayed in the chat interface and stored in short-term session memory.

The available tools are:

- `search_products` - searches the catalog and applies an optional price limit.
- `track_order` - retrieves the status and estimated arrival of a demo order.
- `recommend_products` - selects highly rated products based on preferences and budget.
- `return_policy` - provides the 30-day unused-item return policy.

If the model or Ollama service cannot be reached, the backend uses deterministic offline responses for common shopping, tracking, recommendation, and return queries.

### Key Features

- Product catalog with categories, prices, stock counts, and ratings.
- Product search and category filtering.
- Featured product cards with product details and images.
- Shopping bag with quantity controls and a demo checkout flow.
- Wishlist stored in browser local storage.
- AI Stylist chat with quick prompt suggestions.
- Order tracking for `ORD1001`, `ORD1002`, and `ORD1003`.
- Short-term conversation memory per session.
- Local Ollama model configuration through environment variables.
- Responsive layout for desktop and mobile screens.
- Offline fallback mode for basic assistant behavior.

## 3. Implementation and Results

### Technologies and Tools Used

| Area | Technology |
| --- | --- |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Frontend design | Responsive CSS, DM Sans, Playfair Display, Unsplash product imagery |
| Primary backend | Node.js, Express 4 |
| Alternative backend | Python, FastAPI, Uvicorn, Pydantic, HTTPX |
| AI runtime | Ollama with a local chat model such as `llama3.2:3b` |
| Data storage | In-memory demo catalog, orders, and sessions; browser local storage for bag and wishlist |
| Development tools | npm, Python virtual environment, Git, GitHub |

### Working Process

The project was implemented in the following stages:

1. Defined a demo product catalog, order records, return policy, and agent actions.
2. Built the Express backend and API endpoints for products, chat, configuration, and session reset.
3. Added the equivalent FastAPI backend for Python-based execution.
4. Connected both backends to Ollama through its local chat API.
5. Added tool execution and validation for catalog, order, recommendation, and policy requests.
6. Created the storefront interface with product browsing, shopping bag, wishlist, tracking, and AI Stylist views.
7. Added an offline response path so the interface remains usable when Ollama is stopped.
8. Published the project to GitHub in the `main` branch.

### Screenshots and Output

The implemented interface provides the following views for demonstration screenshots:

- **Home page:** branded storefront hero section and featured products.
- **Shop page:** category tabs, product search, sorting, product cards, and add-to-bag actions.
- **Product page:** product image, category, rating, price, description, color options, and related products.
- **AI Stylist page:** conversational chat panel with quick prompts and assistant responses.
- **Orders page:** order progress display and tracking form.
- **Wishlist and bag pages:** saved products, quantities, totals, and demo checkout.

Example assistant outputs include:

- `ORD1001 is Out for delivery. Estimated arrival: Today, 7 PM.`
- Product recommendations filtered by interests such as audio, footwear, travel, or home.
- Return guidance explaining that unused items may be returned within 30 days and that the demo does not process real refunds.

### Results Achieved

The completed prototype demonstrates the core customer-support workflow from product discovery to conversational assistance. It combines a usable storefront with a local AI agent that can call controlled tools instead of inventing catalog or order information. The fallback mode also allows basic demonstrations without an active Ollama model.

The current result is a functional academic or portfolio prototype. Product, order, session, and checkout data are intentionally demo-only and are not connected to a live commerce platform or payment provider.

## 4. Conclusion and Future Scope

### Project Conclusion

ShopMate AI demonstrates how a local language model can be combined with deterministic e-commerce tools to create a practical customer-support agent. The system gives customers a single conversational entry point while retaining normal storefront workflows such as browsing, wishlist management, cart updates, and order tracking.

The tool-calling design is important because the assistant can retrieve application data before answering. This creates a clearer boundary between language generation and business logic and provides a straightforward path toward production integrations.

### Challenges Faced

- Connecting a local language model to a browser-based chat workflow.
- Ensuring that product and order responses are based on application data.
- Handling model or service unavailability with useful fallback responses.
- Keeping the Node.js and Python backend implementations behaviorally aligned.
- Managing short-term conversation history without a persistent database.
- Making the storefront responsive while supporting several interactive views.

### Future Enhancements

- Add user registration, authentication, and customer profiles.
- Replace in-memory demo data with MySQL, MongoDB, Firebase, or PostgreSQL.
- Add an administrator dashboard for products, inventory, orders, and support conversations.
- Connect real payment, shipping, return, and refund services.
- Add retrieval-augmented generation for store policies and frequently asked questions.
- Add human-agent escalation and conversation analytics.
- Persist session memory using Redis or a database.
- Add voice input, multilingual support, WhatsApp support, and email support.
- Add automated unit, API, and browser tests.
- Deploy the application with secured environment variables and production monitoring.

### References

- Ollama documentation: https://ollama.com/
- Express documentation: https://expressjs.com/
- FastAPI documentation: https://fastapi.tiangolo.com/
- Node.js documentation: https://nodejs.org/docs/latest/api/
- MDN Web Docs: https://developer.mozilla.org/
- Unsplash Source images used by the demo storefront: https://unsplash.com/
