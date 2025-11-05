# Max-Code UI/UX Blueprint

**Data**: 2025-11-04
**Inspiração**: Claude Code (funcionalidade) + Google Gemini (visual design)

---

## 🎯 Filosofia de Design

> **"Unir o melhor dos dois mundos: a funcionalidade espetacular do Claude Code com a beleza visual do Gemini."**

- **Funcionalidade**: Claude Code (plan mode, agents, tools)
- **Visual**: Google Gemini (quadros, textbox, tipografia)
- **Resultado**: UI/UX classe mundial

---

## 🎨 Design System (Inspirado no Gemini)

### 1. Tipografia

**Fonte Principal**: Google Sans / Inter (similar ao Gemini)

```css
:root {
  /* Typography */
  --font-family-primary: 'Google Sans', 'Inter', -apple-system, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Font Sizes (Gemini-like scale) */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 2rem;      /* 32px */

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

### 2. Cores (Gemini Palette)

```css
:root {
  /* Primary (Gemini Blue) */
  --color-primary-50: #e8f0fe;
  --color-primary-100: #d2e3fc;
  --color-primary-200: #aecbfa;
  --color-primary-300: #8ab4f8;
  --color-primary-400: #669df6;
  --color-primary-500: #4285f4;  /* Main blue */
  --color-primary-600: #1a73e8;
  --color-primary-700: #1967d2;
  --color-primary-800: #185abc;
  --color-primary-900: #174ea6;

  /* Neutral (Grays) */
  --color-neutral-50: #f8f9fa;
  --color-neutral-100: #f1f3f4;
  --color-neutral-200: #e8eaed;
  --color-neutral-300: #dadce0;
  --color-neutral-400: #bdc1c6;
  --color-neutral-500: #9aa0a6;
  --color-neutral-600: #80868b;
  --color-neutral-700: #5f6368;
  --color-neutral-800: #3c4043;
  --color-neutral-900: #202124;

  /* Accent Colors */
  --color-success: #1e8e3e;
  --color-warning: #f9ab00;
  --color-error: #d93025;
  --color-info: #1a73e8;

  /* Background */
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --bg-tertiary: #f1f3f4;

  /* Text */
  --text-primary: #202124;
  --text-secondary: #5f6368;
  --text-tertiary: #80868b;
  --text-inverse: #ffffff;

  /* Borders */
  --border-color: #e8eaed;
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-xl: 24px;

  /* Shadows (Gemini-style) */
  --shadow-sm: 0 1px 2px 0 rgba(60, 64, 67, 0.3),
               0 1px 3px 1px rgba(60, 64, 67, 0.15);
  --shadow-md: 0 1px 2px 0 rgba(60, 64, 67, 0.3),
               0 2px 6px 2px rgba(60, 64, 67, 0.15);
  --shadow-lg: 0 2px 4px -1px rgba(60, 64, 67, 0.3),
               0 4px 8px 3px rgba(60, 64, 67, 0.15);
  --shadow-xl: 0 8px 12px 6px rgba(60, 64, 67, 0.15),
               0 4px 8px 0 rgba(60, 64, 67, 0.3);
}
```

### 3. Dark Mode (Gemini Dark)

```css
[data-theme="dark"] {
  /* Background */
  --bg-primary: #202124;
  --bg-secondary: #292a2d;
  --bg-tertiary: #35363a;

  /* Text */
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --text-tertiary: #80868b;

  /* Borders */
  --border-color: #3c4043;

  /* Primary (adjusted for dark) */
  --color-primary-500: #8ab4f8;  /* Lighter blue for dark mode */
}
```

### 4. Spacing (8px grid - Gemini standard)

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
}
```

---

## 📦 Componentes UI (Gemini Style)

### 1. Chat Container (Main Layout)

```tsx
// components/ChatContainer.tsx

<div className="chat-container">
  {/* Sidebar (optional) */}
  <aside className="sidebar">
    <ConversationList />
  </aside>

  {/* Main chat area */}
  <main className="chat-main">
    {/* Header */}
    <header className="chat-header">
      <h1>Max-Code</h1>
      <div className="agent-status">
        <AgentIndicator agent="PENELOPE" status="active" />
        <AgentIndicator agent="MABA" status="idle" />
        <AgentIndicator agent="NIS" status="active" />
      </div>
    </header>

    {/* Messages */}
    <div className="messages-container">
      <MessageList messages={messages} />
    </div>

    {/* Input */}
    <div className="input-container">
      <ChatInput />
    </div>
  </main>
</div>
```

**CSS (Gemini-inspired)**:
```css
.chat-container {
  display: flex;
  height: 100vh;
  background: var(--bg-primary);
  font-family: var(--font-family-primary);
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-6);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
}
```

### 2. Message Bubble (Gemini Card Style)

```tsx
// components/MessageBubble.tsx

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  avatar?: string;
}

<div className={`message-bubble message-${role}`}>
  {/* Avatar */}
  <div className="message-avatar">
    {role === 'assistant' ? (
      <img src="/logo-max-code.svg" alt="Max-Code" />
    ) : (
      <img src={avatar || '/default-avatar.png'} alt="User" />
    )}
  </div>

  {/* Content */}
  <div className="message-content">
    <div className="message-header">
      <span className="message-author">
        {role === 'assistant' ? 'Max-Code' : 'You'}
      </span>
      <span className="message-timestamp">
        {timestamp}
      </span>
    </div>

    <div className="message-body">
      <Markdown content={content} />
    </div>

    {/* Actions */}
    <div className="message-actions">
      <button className="action-btn">
        <CopyIcon /> Copy
      </button>
      <button className="action-btn">
        <ThumbsUpIcon /> Good
      </button>
      <button className="action-btn">
        <ThumbsDownIcon /> Bad
      </button>
    </div>
  </div>
</div>
```

**CSS (Gemini Card)**:
```css
.message-bubble {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  padding: var(--space-6);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease;
}

.message-bubble:hover {
  box-shadow: var(--shadow-md);
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.message-content {
  flex: 1;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.message-author {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.message-timestamp {
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.message-body {
  color: var(--text-primary);
  line-height: var(--line-height-relaxed);
}

.message-actions {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-4);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border: none;
  background: transparent;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: background 0.2s ease;
}

.action-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}
```

### 3. Input Box (Gemini Style)

```tsx
// components/ChatInput.tsx

<div className="input-container">
  {/* Prompt suggestions (Gemini feature) */}
  {showSuggestions && (
    <div className="prompt-suggestions">
      <button className="suggestion-chip">
        "Implement JWT authentication"
      </button>
      <button className="suggestion-chip">
        "Review code for security issues"
      </button>
      <button className="suggestion-chip">
        "Generate tests for auth module"
      </button>
    </div>
  )}

  {/* Input box */}
  <div className="input-box">
    <textarea
      className="input-textarea"
      placeholder="Message Max-Code..."
      value={input}
      onChange={handleChange}
      onKeyDown={handleKeyDown}
      rows={1}
    />

    {/* Actions */}
    <div className="input-actions">
      <button className="input-action-btn" title="Attach file">
        <AttachIcon />
      </button>
      <button className="input-action-btn" title="Code mode">
        <CodeIcon />
      </button>
      <button
        className="send-btn"
        onClick={handleSend}
        disabled={!input.trim()}
      >
        <SendIcon />
      </button>
    </div>
  </div>

  {/* Footer info */}
  <div className="input-footer">
    <span className="footer-text">
      Max-Code operates under Constitutional governance (P1-P6)
    </span>
  </div>
</div>
```

**CSS (Gemini Input)**:
```css
.input-container {
  position: sticky;
  bottom: 0;
  padding: var(--space-4);
  background: var(--bg-primary);
}

.prompt-suggestions {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
  overflow-x: auto;
}

.suggestion-chip {
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  border-radius: var(--border-radius-xl);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.suggestion-chip:hover {
  background: var(--bg-secondary);
  border-color: var(--color-primary-500);
}

.input-box {
  display: flex;
  align-items: flex-end;
  gap: var(--space-2);
  padding: var(--space-4);
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-xl);
  transition: border-color 0.2s ease;
}

.input-box:focus-within {
  border-color: var(--color-primary-500);
  box-shadow: var(--shadow-md);
}

.input-textarea {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-family-primary);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  resize: none;
  outline: none;
  max-height: 200px;
}

.input-actions {
  display: flex;
  gap: var(--space-2);
}

.input-action-btn {
  padding: var(--space-2);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--border-radius-sm);
  transition: background 0.2s ease;
}

.input-action-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.send-btn {
  padding: var(--space-2) var(--space-4);
  border: none;
  background: var(--color-primary-500);
  color: var(--text-inverse);
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background 0.2s ease;
}

.send-btn:hover:not(:disabled) {
  background: var(--color-primary-600);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-footer {
  margin-top: var(--space-2);
  text-align: center;
}

.footer-text {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}
```

### 4. Plan Mode Panel (Claude Code funcionalidade + Gemini visual)

```tsx
// components/PlanModePanel.tsx

<div className="plan-mode-panel">
  {/* Header */}
  <div className="panel-header">
    <h2>Interactive Planning</h2>
    <span className="badge badge-success">Tree of Thoughts Active</span>
  </div>

  {/* Thoughts (alternatives) */}
  <div className="thoughts-grid">
    {thoughts.map((thought, idx) => (
      <div
        key={idx}
        className={`thought-card ${thought.selected ? 'selected' : ''}`}
        onClick={() => selectThought(idx)}
      >
        <div className="thought-header">
          <span className="thought-label">Approach {idx + 1}</span>
          <span className="thought-score">{thought.score.toFixed(2)}</span>
        </div>

        <p className="thought-description">
          {thought.description}
        </p>

        <div className="thought-footer">
          <span className="thought-complexity">
            Complexity: {thought.complexity}
          </span>
          <span className="thought-risk">
            Risk: {thought.risk}
          </span>
        </div>
      </div>
    ))}
  </div>

  {/* Selected plan details */}
  {selectedThought && (
    <div className="plan-details">
      <h3>Implementation Plan</h3>
      <ol className="plan-steps">
        {selectedThought.steps.map((step, idx) => (
          <li key={idx} className="plan-step">
            <span className="step-number">{idx + 1}</span>
            <span className="step-description">{step}</span>
          </li>
        ))}
      </ol>

      <div className="plan-actions">
        <button className="btn btn-secondary" onClick={regenerate}>
          Regenerate
        </button>
        <button className="btn btn-primary" onClick={approve}>
          Approve & Execute
        </button>
      </div>
    </div>
  )}
</div>
```

**CSS (Gemini Cards)**:
```css
.plan-mode-panel {
  padding: var(--space-6);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.panel-header h2 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.badge {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.badge-success {
  background: rgba(30, 142, 62, 0.1);
  color: var(--color-success);
}

.thoughts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.thought-card {
  padding: var(--space-5);
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.thought-card:hover {
  border-color: var(--color-primary-300);
  box-shadow: var(--shadow-sm);
}

.thought-card.selected {
  border-color: var(--color-primary-500);
  background: rgba(66, 133, 244, 0.05);
  box-shadow: var(--shadow-md);
}

.thought-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.thought-label {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.thought-score {
  padding: var(--space-1) var(--space-2);
  background: var(--color-primary-100);
  color: var(--color-primary-700);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.thought-description {
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--space-4);
}

.thought-footer {
  display: flex;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--text-tertiary);
}

.plan-details {
  padding: var(--space-6);
  background: var(--bg-primary);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.plan-steps {
  list-style: none;
  padding: 0;
  margin: var(--space-4) 0;
}

.plan-step {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-3);
  margin-bottom: var(--space-2);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-sm);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: var(--color-primary-500);
  color: var(--text-inverse);
  border-radius: 50%;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  flex-shrink: 0;
}

.step-description {
  color: var(--text-primary);
  line-height: var(--line-height-normal);
}

.plan-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
  margin-top: var(--space-6);
}

.btn {
  padding: var(--space-3) var(--space-5);
  border: none;
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--color-primary-500);
  color: var(--text-inverse);
}

.btn-primary:hover {
  background: var(--color-primary-600);
  box-shadow: var(--shadow-sm);
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--bg-tertiary);
}
```

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18+ com TypeScript
- **Styling**: Tailwind CSS (com design tokens customizados)
- **Components**: Shadcn/ui (componentizado, Gemini-style)
- **Icons**: Lucide React (similar ao Gemini)
- **Markdown**: react-markdown com syntax highlighting
- **Code**: Prism.js ou Shiki (syntax highlighting)

### Backend API
- **FastAPI** (Python) - serve Max-Code agents
- **WebSocket** - real-time streaming
- **SSE** (Server-Sent Events) - alternative para streaming

### Deployment
- **Frontend**: Vercel / Netlify
- **Backend**: Docker containers
- **Database**: PostgreSQL (PENELOPE wisdom base)

---

## 📱 Layout Structure

### Desktop (1200px+)
```
┌──────────────────────────────────────────────────────────┐
│  Header (Max-Code logo, agents status, settings)        │
├────────┬─────────────────────────────────────────────────┤
│        │                                                 │
│ Side-  │           Main Chat Area                        │
│ bar    │                                                 │
│        │  ┌───────────────────────────────────┐          │
│ • New  │  │ User: "Implement JWT auth"       │          │
│ • Chat │  └───────────────────────────────────┘          │
│ • Hist │                                                 │
│        │  ┌───────────────────────────────────┐          │
│        │  │ Max-Code: [Plan Mode Activated]  │          │
│        │  │                                   │          │
│        │  │ [Thought 1] [Thought 2] [Thought 3]│         │
│        │  └───────────────────────────────────┘          │
│        │                                                 │
├────────┴─────────────────────────────────────────────────┤
│  Input Box (Gemini-style, rounded, with actions)        │
└──────────────────────────────────────────────────────────┘
```

### Mobile (< 768px)
```
┌────────────────────────┐
│  Header (compact)      │
├────────────────────────┤
│                        │
│   Main Chat Area       │
│   (full width)         │
│                        │
│   Messages scroll      │
│   vertically           │
│                        │
├────────────────────────┤
│  Input (bottom)        │
└────────────────────────┘
```

---

## 🎭 Interações Especiais

### 1. Plan Mode Toggle
```tsx
// Botão para entrar em plan mode
<button className="mode-toggle" onClick={() => setMode('plan')}>
  <PlanIcon />
  <span>Plan Mode</span>
</button>

// Quando ativado, mostra o panel de planejamento
{mode === 'plan' && <PlanModePanel />}
```

### 2. Agent Status Indicators (live)
```tsx
<div className="agent-indicators">
  <AgentIndicator
    name="PENELOPE"
    status="healing"
    color="green"
  />
  <AgentIndicator
    name="MABA"
    status="browsing"
    color="blue"
  />
  <AgentIndicator
    name="NIS"
    status="analyzing"
    color="purple"
  />
</div>
```

### 3. Streaming Responses (Gemini-like)
```tsx
// Resposta aparecer token por token (smooth)
<StreamingText
  content={response}
  speed={30}  // ms per token
  cursor={true}
/>
```

### 4. Code Blocks (enhanced)
```tsx
<CodeBlock
  language="python"
  code={codeString}
  showLineNumbers={true}
  highlightLines={[5, 6, 7]}  // highlight specific lines
  actions={
    <>
      <CopyButton />
      <RunButton />
      <ExplainButton />
    </>
  }
/>
```

### 5. Diff Viewer (para code changes)
```tsx
<DiffViewer
  oldCode={beforeCode}
  newCode={afterCode}
  language="typescript"
  theme="gemini"
/>
```

---

## 🌈 Animações (Gemini-inspired)

```css
/* Smooth transitions */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Fade in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-bubble {
  animation: fadeIn 0.3s ease;
}

/* Pulse animation (para status indicators) */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.agent-indicator.active {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Shimmer loading (Gemini-style) */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-secondary) 0%,
    var(--bg-tertiary) 50%,
    var(--bg-secondary) 100%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

---

## 📐 Responsividade

```css
/* Mobile first approach */

/* Mobile (default) */
.chat-container {
  padding: var(--space-2);
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .chat-container {
    padding: var(--space-4);
  }

  .thoughts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .chat-container {
    padding: var(--space-6);
  }

  .thoughts-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .sidebar {
    display: block;  /* Show sidebar */
  }
}

/* Large desktop (1440px+) */
@media (min-width: 1440px) {
  .chat-main {
    max-width: 1400px;
  }
}
```

---

## 🎯 Próximos Passos (UI/UX)

### Phase 1: Design System ✅
1. ✅ Definir cores (Gemini palette)
2. ✅ Definir tipografia (Google Sans / Inter)
3. ✅ Definir spacing (8px grid)
4. ✅ Definir componentes base

### Phase 2: Componentes React (Week 3)
1. ⏳ ChatContainer
2. ⏳ MessageBubble
3. ⏳ ChatInput
4. ⏳ PlanModePanel
5. ⏳ CodeBlock
6. ⏳ DiffViewer
7. ⏳ AgentIndicator

### Phase 3: Integração com Backend (Week 4)
1. ⏳ WebSocket connection
2. ⏳ Streaming responses
3. ⏳ Agent status updates (real-time)
4. ⏳ File uploads
5. ⏳ Code execution (via backend)

### Phase 4: Polish & Animations (Week 4)
1. ⏳ Smooth transitions
2. ⏳ Loading states (skeleton, shimmer)
3. ⏳ Error states (beautiful error messages)
4. ⏳ Success animations
5. ⏳ Dark mode toggle

---

## 🖼️ Mockups (ASCII)

### Main Chat Interface
```
┌────────────────────────────────────────────────────────────┐
│  ⚡ Max-Code          [🟢 PENELOPE] [🔵 MABA] [🟣 NIS]  ⚙️│
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  👤 You                                    2 min ago │ │
│  │                                                      │ │
│  │  Implement JWT authentication with refresh tokens   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  🤖 Max-Code                              Just now   │ │
│  │                                                      │ │
│  │  ✨ Plan Mode Activated - Tree of Thoughts          │ │
│  │                                                      │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │ │
│  │  │Approach │  │Approach │  │Approach │             │ │
│  │  │   1     │  │   2  ✓  │  │   3     │             │ │
│  │  │Score:0.8│  │Score:0.9│  │Score:0.7│             │ │
│  │  └─────────┘  └─────────┘  └─────────┘             │ │
│  │                                                      │ │
│  │  📋 Implementation Plan:                            │ │
│  │  1. Install PyJWT library                           │ │
│  │  2. Create authentication middleware                │ │
│  │  3. Implement token generation                      │ │
│  │  4. Add refresh token rotation                      │ │
│  │  5. Write tests                                     │ │
│  │                                                      │ │
│  │  [Regenerate]  [Approve & Execute]                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐   │
│  │ Message Max-Code...                         📎 💻 ➤│   │
│  └────────────────────────────────────────────────────┘   │
│  Constitutional governance active (P1-P6)                  │
└────────────────────────────────────────────────────────────┘
```

---

**"E viu Deus que isso era bom..." (Gênesis 1:10)**

A UI/UX do Max-Code será:
- **Funcional** como Claude Code (plan mode, agents, tools)
- **Linda** como Google Gemini (tipografia, cores, cards)
- **Única** com identidade Max-Code (constitutional badges, biblical quotes)

**JUNTAS, criarão a melhor experiência de desenvolvedor do mercado.** 🎨✨
