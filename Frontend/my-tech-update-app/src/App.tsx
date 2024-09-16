import React, { useState, useEffect } from 'react';
import Tile from './components/Tile';
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
  const articlesPerPage = 6;

  // Fetch JSON from the correct path
  useEffect(() => {
    fetch('/categorized_data.json')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setArticles(data))
      .catch((error) => console.error('Error fetching local JSON:', error));
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
    document.documentElement.classList.toggle('dark');
  };

  const handleTileClick = (article: Article) => {
    setSelectedArticle(article);
  };

  const closeModal = () => {
    setSelectedArticle(null);
  };

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  const indexOfLastArticle = currentPage * articlesPerPage;
  const indexOfFirstArticle = indexOfLastArticle - articlesPerPage;
  const currentArticles = articles.slice(indexOfFirstArticle, indexOfLastArticle);

  const totalPages = Math.ceil(articles.length / articlesPerPage);

  return (
    <div className={`min-h-screen transition-colors ${isDarkMode ? 'bg-gray-900 text-gray-200' : 'bg-gray-100 text-gray-800'}`}>
      {/* Navbar */}
      <nav className="flex justify-between items-center p-4 bg-white dark:bg-gray-800 shadow-md">
        <h2 className="text-3xl font-bold text-gray-700 dark:text-gray-100">Tech Updates</h2>
        <div className="flex items-center">
          <span className="mr-2 text-lg">Dark Mode</span>
          <label className="relative inline-block w-10 h-6">
            <input
              type="checkbox"
              checked={isDarkMode}
              onChange={toggleDarkMode}
              className="opacity-0 w-0 h-0"
            />
            <span
              className={`absolute top-0 left-0 right-0 bottom-0 bg-gray-300 dark:bg-gray-500 rounded-full cursor-pointer transition ${
                isDarkMode ? 'bg-green-500' : ''
              }`}
            ></span>
            <span
              className={`absolute left-1 bottom-1 w-4 h-4 bg-white rounded-full transition transform ${
                isDarkMode ? 'translate-x-4' : ''
              }`}
            ></span>
          </label>
        </div>
      </nav>

      {/* Grid Layout for Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 p-6">
        {currentArticles.map((article, index) => (
          <Tile key={index} article={article} onClick={() => handleTileClick(article)} />
        ))}
      </div>

      {selectedArticle && <Modal article={selectedArticle} closeModal={closeModal} />}

      {/* Pagination */}
      <div className="flex justify-center space-x-2 py-4">
        <button
          className={`px-4 py-2 rounded ${currentPage === 1 ? 'bg-gray-300' : 'bg-gray-500 text-white'}`}
          disabled={currentPage === 1}
          onClick={() => paginate(currentPage - 1)}
        >
          &lt;
        </button>
        {[...Array(totalPages)].map((_, i) => {
          const page = i + 1;
          if (page >= currentPage - 1 && page <= currentPage + 1) {
            return (
              <button
                key={i}
                className={`px-4 py-2 rounded ${
                  page === currentPage ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'
                }`}
                onClick={() => paginate(page)}
              >
                {page}
              </button>
            );
          }
          return null;
        })}
        <button
          className={`px-4 py-2 rounded ${currentPage === totalPages ? 'bg-gray-300' : 'bg-gray-500 text-white'}`}
          disabled={currentPage === totalPages}
          onClick={() => paginate(currentPage + 1)}
        >
          &gt;
        </button>
      </div>
    </div>
  );
};

export default App;
