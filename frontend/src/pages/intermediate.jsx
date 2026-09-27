import ReactMarkdown from "react-markdown";
import { useState } from "react";
import { Link } from "react-router-dom";
import "../App.css";


function Intermediate() {

  const [selectedMode, setSelectedMode] = useState("simple");
  
const [question, setQuestion] = useState("");
const [answer, setAnswer] = useState("");
const [sources, setSources] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

const [uploadedFile, setUploadedFile] = useState(null);
const [uploading, setUploading] = useState(false);
const [uploadMessage, setUploadMessage] = useState("");



const askQuestion = async () => {

  if (!question.trim()) {
    setError("Please enter a question.");
    return;
  }

  setLoading(true);
  setError("");
  setAnswer("");
  setSources([]);

  try {

    const response = await fetch(
      "http://127.0.0.1:8000/ask",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          question: question,
          mode: selectedMode
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Something went wrong."
      );
    }

    setAnswer(String(data.answer || ""));
    setSources(data.sources || []);

  } catch (err) {

    setError(
      err.message || "Unable to connect to LearnLens AI."
    );

  } finally {

    setLoading(false);

  }
};

const uploadDocument = async (file) => { 
    if (!file)
     return; 
    setUploading(true); 
    setUploadMessage("");
     setError(""); 
    const formData = new FormData(); 
    formData.append("file", file); 
    try { 
        const response = await fetch( "http://127.0.0.1:8000/upload", { method: "POST", body: formData } ); 
const data = await response.json(); 
if (!response.ok) { 
    throw new Error( data.detail || "Upload failed." ); } 
setUploadedFile({ name: data.filename, chunks: data.chunk_count }); 
setUploadMessage( `Document processed successfully — ${data.chunk_count} chunks created.` ); } 
catch (err) {
     setError( err.message || "Unable to upload document." ); } 
finally {
     setUploading(false);
     } };



  return (
    <div className="page">

      {/* Navbar */}
      <div className="page-navbar">

        <Link to="/" className="back-link">
          ← LearnLens AI
        </Link>

        <span className="page-level intermediate-text">
          INTERMEDIATE
        </span>

      </div>


      {/* Main Workspace */}
      <main className="workspace">

        <div className="workspace-badge">
          🚀 Intermediate RAG
        </div>

        <h1>
          Document Q&A
        </h1>

        <p className="workspace-description">
          Upload your study material, choose how you want to learn,
          and ask questions grounded in your document.
        </p>


        {/* Upload Section */}
        <div className="rag-section">

          <div className="section-title">

            <span>📄</span>

            <div>
              <h3>Upload your document</h3>
              <p>PDF or TXT files supported</p>
            </div>

          </div>


          <div className="upload-box">

            <div className="upload-icon">
              📁
            </div>

            <h3>
              Drop your document here
            </h3>

            <p>
              or choose a file from your computer
            </p>

                
     <input
      type="file"
      id="document-upload"
      accept=".pdf,.txt"
      style={{ display: "none" }}
      onChange={(e) => {
       const file = e.target.files[0];
       uploadDocument(file);
  }}
/>

<label
  htmlFor="document-upload"
  className="upload-button"
>
  {uploading ? "Processing..." : "Choose File"}
</label>

{uploadedFile && (
  <div
    style={{
      marginTop: "18px",
      padding: "14px",
      borderRadius: "10px",
      background: "rgba(99, 102, 241, 0.08)",
      border: "1px solid rgba(129, 140, 248, 0.2)"
    }}
  >
    <strong>📄 {uploadedFile.name}</strong>

    <p
      style={{
        margin: "6px 0 0",
        color: "#aaaabc",
        fontSize: "12px"
      }}
    >
      {uploadedFile.chunks} chunks indexed and ready for questions.
    </p>
  </div>
)}

{uploadMessage && (
  <p
    style={{
      marginTop: "12px",
      color: "#a5b4fc",
      fontSize: "13px"
    }}
  >
    ✓ {uploadMessage}
  </p>
)}




          </div>

        </div>


        {/* Learning Modes */}
        <div className="rag-section">

          <div className="section-title">

            <span>🎓</span>

            <div>
              <h3>
                How do you want to learn?
              </h3>

              <p>
                Choose a response style for LearnLens AI
              </p>
            </div>

          </div>


          <div className="mode-grid">


            {/* Simple */}
            <button
              className={`mode-card ${
                selectedMode === "simple"
                  ? "active-mode"
                  : ""
              }`}
              onClick={() => setSelectedMode("simple")}
            >

              <span className="mode-icon">
                🟢
              </span>

              <div>

                <h4>
                  Simple
                </h4>

                <p>
                  Explain like I'm a beginner
                </p>

              </div>

            </button>


            {/* Exam */}
            <button
              className={`mode-card ${
                selectedMode === "exam"
                  ? "active-mode"
                  : ""
              }`}
              onClick={() => setSelectedMode("exam")}
            >

              <span className="mode-icon">
                🔵
              </span>

              <div>

                <h4>
                  Exam
                </h4>

                <p>
                  Structured exam-style answer
                </p>

              </div>

            </button>


            {/* Revision */}
            <button
              className={`mode-card ${
                selectedMode === "revision"
                  ? "active-mode"
                  : ""
              }`}
              onClick={() => setSelectedMode("revision")}
            >

              <span className="mode-icon">
                🟡
              </span>

              <div>

                <h4>
                  Revision
                </h4>

                <p>
                  Short bullets and keywords
                </p>

              </div>

            </button>


            {/* Viva */}
            <button
              className={`mode-card ${
                selectedMode === "viva"
                  ? "active-mode"
                  : ""
              }`}
              onClick={() => setSelectedMode("viva")}
            >

              <span className="mode-icon">
                🟣
              </span>

              <div>

                <h4>
                  Viva
                </h4>

                <p>
                  Concept + possible viva questions
                </p>

              </div>

            </button>


          </div>

        </div>


        {/* Question Section */}
        <div className="rag-section">

          <div className="section-title">

            <span>💬</span>

            <div>

              <h3>
                Ask your question
              </h3>

              <p>
                LearnLens AI will answer using your document
              </p>

            </div>

          </div>


          <div className="question-box">

            <textarea
              placeholder="e.g. What is a LEFT JOIN?"
              rows="4"
              value={question} 
              onChange={(e) => setQuestion(e.target.value)}
            />

            
       <button
       className="ask-button"
    onClick={askQuestion}
     disabled={loading}
    >
  {loading ? "Thinking..." : "Ask LearnLens →"}
</button>

        {error && (
         <p style={{ color: "#f87171", marginTop: "10px" }}>
         {error}
         </p>
)}

          </div>

        </div>


        {/* Answer */}
        <div className="rag-section answer-section">

          <div className="section-title">

            <span>🤖</span>

            <div>

              <h3>
                Answer
              </h3>

              <p>
                Evidence-grounded response
              </p>

            </div>

          </div>


          <div className="answer-box">

           
         {answer ? (
          <div className="answer-content"> 
          <ReactMarkdown children={String(answer || "")} />
            </div>
         
          
      ) : (
         <p className="answer-placeholder">
         Your answer will appear here after you ask a question.
          </p>
         )}



          </div>

        </div>


        {/* Sources */}
        <div className="rag-section">

          <div className="section-title">

            <span>📚</span>

            <div>

              <h3>
                Sources
              </h3>

              <p>
                Supporting evidence from your document
              </p>

            </div>

          </div>


          
{sources.length > 0 ? (
  sources.map((source, index) => (
    <div
      key={index}
      style={{
        padding: "14px",
        marginBottom: "10px",
        borderRadius: "10px",
        background: "rgba(0, 0, 0, 0.18)"
      }}
    >
      <strong>
        Source {index + 1}
        {source.page ? ` — Page ${source.page}` : ""}
      </strong>

      <p
        style={{
          margin: "8px 0 0",
          color: "#aaaabc",
          lineHeight: "1.6",
          fontSize: "13px"
        }}
      >
        {source.chunk}
      </p>
    </div>
  ))
) : (
  <div className="sources-empty">
    Sources will appear here with page numbers.
  </div>
)}



        </div>


      </main>

    </div>
  );
}


export default Intermediate;

