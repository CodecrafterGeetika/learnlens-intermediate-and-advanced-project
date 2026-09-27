import { Link } from "react-router-dom";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "../App.css";

function Advanced() {

  const [selectedFile, setSelectedFile] = useState(null);

  const [documents, setDocuments] = useState([]);
  const [documentId, setDocumentId] = useState(null);

  const [uploadMessage, setUploadMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("simple");

  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [asking, setAsking] = useState(false);

  const [rewrittenQuery, setRewrittenQuery] = useState("");
  const [fallbackUsed, setFallbackUsed] = useState(false);
  const [grounded, setGrounded] = useState(false);


  // =========================
  // UPLOAD DOCUMENT
  // =========================

  const handleUpload = async () => {

    if (!selectedFile) {
      setUploadMessage("Please choose a document first.");
      return;
    }

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {

      setUploading(true);
      setUploadMessage("");

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed."
        );
      }

      // Add uploaded document to the list
      setDocuments((previousDocuments) => [
        ...previousDocuments,
        {
          document_id: data.document_id,
          filename: data.filename
        }
      ]);

      // Automatically select the newly uploaded document
      setDocumentId(data.document_id);

      setUploadMessage(
        `Uploaded successfully: ${data.filename}`
      );

      setSelectedFile(null);

    } catch (error) {

      setUploadMessage(
        `Upload failed: ${error.message}`
      );

    } finally {

      setUploading(false);

    }
  };


  // =========================
  // ASK QUESTION
  // =========================

  const handleAsk = async () => {

    // Check whether at least one document exists
    if (documents.length === 0) {

      setAnswer(
        "Please upload a document first."
      );

      return;
    }

    // Check question
    if (!question.trim()) {

      setAnswer(
        "Please enter a question."
      );

      return;
    }

    try {

      setAsking(true);

      setAnswer("");
      setSources([]);
      setRewrittenQuery("");
      setFallbackUsed(false);
      setGrounded(false);

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            question: question,

            mode: mode,

            // null = search across ALL documents
            document_id: documentId

          })
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail || "Question failed."
        );

      }

      // Store answer
      setAnswer(data.answer);

      // Store sources
      setSources(data.sources || []);

      // Store rewritten query
      setRewrittenQuery(
        data.rewritten_query || ""
      );

      // Store fallback status
      setFallbackUsed(
        data.fallback_used || false
      );

      // Store grounded status
      setGrounded(
        data.grounded || false
      );

    } catch (error) {

      setAnswer(
        `Error: ${error.message}`
      );

    } finally {

      setAsking(false);

    }
  };


  // =========================
  // UI
  // =========================

  return (

    <div className="page">

      {/* =========================
          NAVBAR
      ========================= */}

      <div className="page-navbar">

        <Link
          to="/"
          className="back-link"
        >
          ← LearnLens AI
        </Link>

        <span className="page-level advanced-text">
          ADVANCED
        </span>

      </div>


      <main className="workspace">

        {/* =========================
            HEADER
        ========================= */}

        <div className="workspace-badge advanced-workspace-badge">
          🧠 Advanced RAG
        </div>

        <h1>
          Advanced Intelligence
        </h1>

        <p className="workspace-description">

          A production-style RAG architecture designed for
          deeper retrieval, stronger grounding, and richer
          document learning workflows.

        </p>


        {/* =========================
            FEATURE PREVIEW
        ========================= */}

        <div className="feature-preview">

          <div>

            <span>🔀</span>

            <h3>
              Hybrid Search
            </h3>

            <p>
              Semantic + keyword retrieval
            </p>

          </div>


          <div>

            <span>🎯</span>

            <h3>
              Reranking
            </h3>

            <p>
              Improve retrieval relevance
            </p>

          </div>


          <div>

            <span>📚</span>

            <h3>
              Multi-Document
            </h3>

            <p>
              Search across documents
            </p>

          </div>


          <div>

            <span>🎤</span>

            <h3>
              Viva Mode
            </h3>

            <p>
              Interactive learning
            </p>

          </div>

        </div>


        <div className="advanced-workspace">


          {/* =========================
              DOCUMENT UPLOAD
          ========================= */}

          <div className="advanced-section">

            <h2>
              📄 Upload Document
            </h2>

            <p>

              Upload a PDF, TXT, or Markdown document
              to build your searchable knowledge base.

            </p>


            {/* DOCUMENT HEADER */}

            <div className="document-header">

              <div>

                <h2>
                  📚 Your Documents
                </h2>

                <p>
                  Select a document or search across
                  all uploaded documents.
                </p>

              </div>


              {/* ADD DOCUMENT */}

              <label className="add-document-button">

                ＋ Add Document

                <input
                  type="file"
                  accept=".pdf,.txt,.md"
                  onChange={(event) => {

                    const file =
                      event.target.files[0];

                    if (!file) return;

                    setSelectedFile(file);

                    setUploadMessage("");

                  }}
                />

              </label>

            </div>


            {/* SELECTED FILE */}

            {selectedFile && (

              <div className="selected-file">

                <div>

                  <span>📄</span>

                  <div>

                    <strong>
                      {selectedFile.name}
                    </strong>

                    <small>
                      Ready to upload
                    </small>

                  </div>

                </div>


                <button
                  className="upload-small-button"
                  onClick={handleUpload}
                  disabled={uploading}
                >

                  {uploading
                    ? "Uploading..."
                    : "Upload"}

                </button>

              </div>

            )}


            {/* UPLOAD MESSAGE */}

            {uploadMessage && (

              <p>
                {uploadMessage}
              </p>

            )}


            {/* DOCUMENT LIST */}

            {documents.length > 0 && (

              <div className="document-list">

                <h3>
                  📚 Uploaded Documents
                </h3>


                {/* =========================
                    ALL DOCUMENTS
                ========================= */}

                <div
                  className={
                    `document-item ${
                      documentId === null
                        ? "selected-document"
                        : ""
                    }`
                  }

                  onClick={() =>
                    setDocumentId(null)
                  }
                >

                  <span>
                    📚 All Documents
                  </span>

                  {documentId === null && (

                    <span>
                      ✓
                    </span>

                  )}

                </div>


                {/* =========================
                    INDIVIDUAL DOCUMENTS
                ========================= */}

                {documents.map((document) => (

                  <div
                    key={document.document_id}

                    className={
                      `document-item ${
                        documentId ===
                        document.document_id
                          ? "selected-document"
                          : ""
                      }`
                    }

                    onClick={() =>
                      setDocumentId(
                        document.document_id
                      )
                    }
                  >

                    <span>
                      📄 {document.filename}
                    </span>


                    {documentId ===
                      document.document_id && (

                      <span>
                        ✓
                      </span>

                    )}

                  </div>

                ))}

              </div>

            )}

          </div>


          {/* =========================
              LEARNING MODES
          ========================= */}

          <div className="advanced-section">

            <h2>
              🎓 Choose Learning Mode
            </h2>

            <p>

              Choose how LearnLens should explain
              the answer.

            </p>


            <div className="mode-selector">

              <div className="mode-options">


                {/* SIMPLE */}

                <button
                  type="button"

                  className={
                    mode === "simple"
                      ? "mode-option active"
                      : "mode-option"
                  }

                  onClick={() =>
                    setMode("simple")
                  }
                >

                  <strong>
                    🧠 Simple
                  </strong>

                  <span>
                    Beginner explanation
                  </span>

                </button>


                {/* EXAM */}

                <button
                  type="button"

                  className={
                    mode === "exam"
                      ? "mode-option active"
                      : "mode-option"
                  }

                  onClick={() =>
                    setMode("exam")
                  }
                >

                  <strong>
                    📝 Exam
                  </strong>

                  <span>
                    Structured answer
                  </span>

                </button>


                {/* REVISION */}

                <button
                  type="button"

                  className={
                    mode === "revision"
                      ? "mode-option active"
                      : "mode-option"
                  }

                  onClick={() =>
                    setMode("revision")
                  }
                >

                  <strong>
                    ⚡ Revision
                  </strong>

                  <span>
                    Quick points
                  </span>

                </button>


                {/* VIVA */}

                <button
                  type="button"

                  className={
                    mode === "viva"
                      ? "mode-option active"
                      : "mode-option"
                  }

                  onClick={() =>
                    setMode("viva")
                  }
                >

                  <strong>
                    🎤 Viva
                  </strong>

                  <span>
                    Practice questions
                  </span>

                </button>

              </div>

            </div>

          </div>


          {/* =========================
              ASK QUESTION
          ========================= */}

          <div className="advanced-section">

            <h2>
              💬 Ask Your Documents
            </h2>

            <textarea

              placeholder={
                documentId === null
                  ? "Ask a question across all uploaded documents..."
                  : "Ask a question about your document..."
              }

              rows="4"

              value={question}

              onChange={(event) =>
                setQuestion(
                  event.target.value
                )
              }

            />


            <button
              className="workspace-button"

              onClick={handleAsk}

              disabled={asking}
            >

              {asking
                ? "Thinking..."
                : "Ask LearnLens"}

            </button>

          </div>


          {/* =========================
              ANSWER
          ========================= */}

          <div className="advanced-section">

            <h2>
              ✨ Answer
            </h2>


            {answer ? (

              <>

                {/* GROUNDED BADGE */}

                <div className="grounded-badge">

                  {grounded

                    ? "✓ Grounded in your document"

                    : "⚠️ Not sufficiently grounded"}

                </div>


                {/* MARKDOWN ANSWER */}

                <div className="answer-placeholder markdown-answer">

                  <ReactMarkdown>
                    {answer}
                  </ReactMarkdown>

                </div>

              </>

            ) : (

              <div className="answer-placeholder">

                Your grounded answer will appear here.

              </div>

            )}

          </div>


          {/* =========================
              RETRIEVAL INSIGHTS
          ========================= */}

          <div className="advanced-section">

            <h2>
              ⚙️ Retrieval Insights
            </h2>


            <div className="retrieval-insights">


              <div>

                <strong>
                  Query Rewriting
                </strong>

                <span>
                  ✓
                </span>

              </div>


              <div>

                <strong>
                  Hybrid Search
                </strong>

                <span>
                  ✓
                </span>

              </div>


              <div>

                <strong>
                  Reranking
                </strong>

                <span>
                  ✓
                </span>

              </div>


              <div>

                <strong>
                  Groundedness Check
                </strong>

                <span>
                  {grounded
                    ? "✓"
                    : "✗"}
                </span>

              </div>


              <div>

                <strong>
                  Fallback Retrieval
                </strong>

                <span>

                  {fallbackUsed
                    ? "✓ Used"
                    : "Not needed"}

                </span>

              </div>

            </div>


            {/* REWRITTEN QUERY */}

            {rewrittenQuery && (

              <div className="rewritten-query">

                <strong>
                  🔎 Rewritten Query
                </strong>

                <p>
                  {rewrittenQuery}
                </p>

              </div>

            )}

          </div>


          {/* =========================
              SOURCES
          ========================= */}

          <div className="advanced-section">

            <h2>
              📚 Sources
            </h2>


            <div className="answer-placeholder">

              {sources.length === 0

                ? "Retrieved document sources will appear here."

                : sources.map(
                    (source, index) => (

                      <div
                        key={
                          `${source.document_id}-${source.chunk_id}-${index}`
                        }
                      >

                        <strong>

                          📄 {source.filename}

                        </strong>


                        <p>

                          Page:{" "}
                          {source.page ?? "N/A"}

                        </p>


                        <p>

                          {source.content}

                        </p>


                        <hr />

                      </div>

                    )
                  )}

            </div>

          </div>


        </div>

      </main>

    </div>
  );
}

export default Advanced;