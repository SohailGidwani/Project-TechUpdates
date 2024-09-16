import React from 'react';

interface TileProps {
  article: {
    Title: string;
    Details: string;
    URL: string;
    Source: string;
    Category: string;
  };
  onClick: () => void;
}
interface Article {
    Title: string;
    Details: string;
    URL: string;
    Source: string;
    Category: string;
  }

const Tile: React.FC<{ article: Article; onClick: () => void }> = ({ article, onClick }) => {
    return (
      <div
        onClick={onClick}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 transition transform hover:scale-105 cursor-pointer"
      >
        <h3 className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100">{article.Title}</h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3">{article.Details}</p>
        <a
          href={article.URL}
          className="text-blue-500 dark:text-blue-400 mt-4 block"
          target="_blank"
          rel="noopener noreferrer"
        >
          Read more at {article.Source}
        </a>
      </div>
    );
  };
  
  export default Tile;
  