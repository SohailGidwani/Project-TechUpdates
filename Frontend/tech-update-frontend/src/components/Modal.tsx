import React from 'react';

interface Article {
  Title: string;
  Details: string;
  URL: string;
  Source: string;
  Category: string;
}

interface ModalProps {
  article: Article;
  closeModal: () => void;
}

const Modal: React.FC<ModalProps> = ({ article, closeModal }) => {
  return (
    <div className="modal-backdrop" onClick={closeModal}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>{article.Title}</h2>
        <p>{article.Details}</p>
        <p><strong>Source:</strong> {article.Source}</p>
        <p><strong>Category:</strong> {article.Category}</p>
        <a href={article.URL} target="_blank" rel="noopener noreferrer">Read More</a>
      </div>
    </div>
  );
};

export default Modal;