
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./App.css";

import Intermediate from "./pages/intermediate";
import Advanced from "./pages/advanced";


function Home() {
  return (
    <div className="app">

      {/* Navbar */}
      <nav className="navbar">

        <div className="logo">
          <span className="logo-icon">✦</span>
          LearnLens AI
        </div>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>

          <a href="#features" className="nav-button">
            Explore
          </a>
        </div>

      </nav>


      {/* Hero Section */}
      <section className="hero">

        <div className="hero-badge">
          ✨ Evidence-Grounded Learning Assistant
        </div>

        <h1>
          One document.
          <br />
          <span>Four ways to learn.</span>
        </h1>

        <p className="hero-description">
          Turn your PDFs and notes into an intelligent learning
          assistant that explains, summarizes, revises, and prepares
          you for viva questions.
        </p>

        <div className="hero-buttons">

          <a href="#features" className="primary-button">
            Get Started →
          </a>

          <a href="#features" className="secondary-button">
            Explore Projects
          </a>

        </div>

      </section>


      {/* Project Cards */}
      <section className="projects" id="features">

        <div className="section-heading">

          <p className="section-label">
            CHOOSE YOUR EXPERIENCE
          </p>

          <h2>
            From <span>RAG fundamentals</span> to advanced intelligence.
          </h2>

          <p>
            LearnLens AI evolves from a complete document Q&A system
            into an advanced retrieval-augmented generation platform.
          </p>

        </div>


        <div className="project-grid">

          {/* Intermediate */}
          <div className="project-card intermediate-card">

            <div className="card-top">

              <div className="project-icon">
                🚀
              </div>

              <span className="level-badge">
                INTERMEDIATE
              </span>

            </div>

            <h3>
              Document Q&A
            </h3>

            <p>
              Upload a PDF or TXT document, ask questions,
              and receive evidence-grounded answers with
              source pages.
            </p>

            <div className="technology-list">
              <span>FastAPI</span>
              <span>FAISS</span>
              <span>Embeddings</span>
              <span>Groq</span>
            </div>

            <Link
              to="/intermediate"
              className="card-button"
            >
              Explore Intermediate →
            </Link>

          </div>


          {/* Advanced */}
          <div className="project-card advanced-card">

            <div className="card-top">

              <div className="project-icon">
                🧠
              </div>

              <span className="level-badge advanced-badge">
                ADVANCED
              </span>

            </div>

            <h3>
              Advanced RAG
            </h3>

            <p>
              A deeper RAG architecture with hybrid retrieval,
              reranking, multi-document reasoning, grounding
              verification, and intelligent learning workflows.
            </p>

            <div className="technology-list">
              <span>Hybrid Search</span>
              <span>Reranking</span>
              <span>Multi-Doc</span>
              <span>Evaluation</span>
            </div>

            <Link
              to="/advanced"
              className="card-button"
            >
              Explore Advanced →
            </Link>

          </div>

        </div>

      </section>


      {/* How it works */}
      <section
        className="how-it-works"
        id="how-it-works"
      >

        <div className="section-heading">

          <p className="section-label">
            HOW IT WORKS
          </p>

          <h2>
            From document to <span>understanding.</span>
          </h2>

        </div>


        <div className="steps">

          <div className="step">
            <div className="step-number">01</div>

            <h3>
              Upload
            </h3>

            <p>
              Upload your PDF or text document.
            </p>
          </div>


          <div className="step">
            <div className="step-number">02</div>

            <h3>
              Retrieve
            </h3>

            <p>
              Relevant information is retrieved using semantic search.
            </p>
          </div>


          <div className="step">
            <div className="step-number">03</div>

            <h3>
              Understand
            </h3>

            <p>
              The AI generates answers grounded in your document.
            </p>
          </div>


          <div className="step">
            <div className="step-number">04</div>

            <h3>
              Learn
            </h3>

            <p>
              Learn through explanations, revision, and viva preparation.
            </p>
          </div>

        </div>

      </section>


      {/* Footer */}
      <footer>

        <div className="logo">
          <span className="logo-icon">✦</span>
          LearnLens AI
        </div>

        <p>
          Evidence-grounded learning from your documents.
        </p>

      </footer>

    </div>
  );
}


function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/intermediate"
          element={<Intermediate />}
        />

        <Route
          path="/advanced"
          element={<Advanced />}
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;

