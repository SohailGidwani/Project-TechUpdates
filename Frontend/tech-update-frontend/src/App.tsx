// src/App.tsx
// import React, { useState, useEffect } from 'react';
// import Tile from './components/Tile';
// import './App.css';

// interface Article {
//   Title: string;
//   Details: string;
//   URL: string;
//   Source: string;
//   Category: string;
// }

// const App: React.FC = () => {
//   const [articles, setArticles] = useState<Article[]>([]);

//   useEffect(() => {
//     // Fetch the local JSON file
//     fetch('/categorized_data.json')
//       .then((response) => response.json())
//       .then((data) => setArticles(data))
//       .catch((error) => console.error('Error fetching local JSON:', error));
//   }, []);

//   return (
//     <div className="app">
//       <h1>Tech Updates</h1>
//       <div className="grid-container">
//         {articles.map((article, index) => (
//           <Tile key={index} article={article} />
//         ))}
//       </div>
//     </div>
//   );
// };

// export default App;

import React, { useState, useEffect } from 'react';
import Tile from './components/Tile';
import './App.css';
import Modal from './components/Modal';

interface Article {
  Title: string;
  Details: string;
  URL: string;
  Source: string;
  Category: string;
}

const App: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const articlesPerPage = 6; // Display 6 tiles per page

  useEffect(() => {
    // Fetch the local JSON file
    fetch('/categorized_data.json')
      .then((response) => response.json())
      .then((data) => setArticles(data))
      .catch((error) => console.error('Error fetching local JSON:', error));
  }, []);

  // Synchronize the dark mode with the body class
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  const handleTileClick = (article: Article) => {
    setSelectedArticle(article);
  };

  const closeModal = () => {
    setSelectedArticle(null);
  };

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  // Pagination logic
  const indexOfLastArticle = currentPage * articlesPerPage;
  const indexOfFirstArticle = indexOfLastArticle - articlesPerPage;
  const currentArticles = articles.slice(indexOfFirstArticle, indexOfLastArticle);

  const totalPages = Math.ceil(articles.length / articlesPerPage);

  return (
    <div className="app">
      <nav className="navbar">
        <h2>Tech Updates</h2>
        <div className="theme-toggle">
          <label className="switch">
            <input type="checkbox" checked={isDarkMode} onChange={toggleDarkMode} />
            <span className="slider round"></span>
          </label>
        </div>
      </nav>

      <div className="grid-container">
        {currentArticles.map((article, index) => (
          <Tile key={index} article={article} onClick={() => handleTileClick(article)} />
        ))}
      </div>

      {selectedArticle && <Modal article={selectedArticle} closeModal={closeModal} />}

      <div className="pagination">
        <button disabled={currentPage === 1} onClick={() => paginate(currentPage - 1)}>
          &lt;
        </button>
        {[...Array(totalPages)].map((_, i) => {
          const page = i + 1;
          if (page >= currentPage - 1 && page <= currentPage + 1) {
            return (
              <button
                key={i}
                onClick={() => paginate(page)}
                className={page === currentPage ? 'active' : ''}
              >
                {page}
              </button>
            );
          }
          return null;
        })}
        <button disabled={currentPage === totalPages} onClick={() => paginate(currentPage + 1)}>
          &gt;
        </button>
      </div>
    </div>
  );
};

export default App;
