import React from 'react';

interface ModalProps {
  article: {
    Title: string;
    Details: string;
    URL: string;
    Source: string;
    Category: string;
  };
  closeModal: () => void;
}

const Modal: React.FC<ModalProps> = ({ article, closeModal }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={closeModal}>
      <div
        className="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-lg w-full mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-2xl font-bold mb-4">{article.Title}</h3>
        <p className="text-gray-700 dark:text-gray-300 mb-4">{article.Details}</p>
        <a
          href={article.URL}
          className="text-blue-500 hover:underline dark:text-blue-400"
          target="_blank"
          rel="noopener noreferrer"
        >
          Read more at {article.Source}
        </a>
      </div>
    </div>
  );
};

export default Modal;
