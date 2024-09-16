// // src/components/Tile.tsx
// import React from 'react';

// interface Article {
//   Title: string;
//   Details: string;
//   URL: string;
//   Source: string;
//   Category: string;
// }

// interface TileProps {
//   article: Article;
// }

// const Tile: React.FC<TileProps> = ({ article }) => {
//   const handleUpvote = () => {
//     console.log(`Upvoted: ${article.Title}`);
//   };

//   const handleShare = () => {
//     navigator.clipboard.writeText(article.URL);
//     alert('Link copied to clipboard!');
//   };

//   return (
//     <div className="tile">
//       <h2>{article.Title}</h2>
//       <p>{article.Details}</p>
//       <p><strong>Source:</strong> {article.Source}</p>
//       <p><strong>Category:</strong> {article.Category}</p>
//       <a href={article.URL} target="_blank" rel="noopener noreferrer">Read More</a>
//       <div className="tile-actions">
//         <button onClick={handleUpvote}>Upvote</button>
//         <button onClick={handleShare}>Share</button>
//       </div>
//     </div>
//   );
// };

// export default Tile;

import React from 'react';

interface Article {
  Title: string;
  Details: string;
  URL: string;
  Source: string;
  Category: string;
}

interface TileProps {
  article: Article;
  onClick: () => void;
}

const Tile: React.FC<TileProps> = ({ article, onClick }) => {
  return (
    <div className="tile" onClick={onClick}>
      <h2>{article.Title}</h2>
      <p>{article.Details.slice(0, 100)}...</p>
      <p><strong>Source:</strong> {article.Source}</p>
      <p><strong>Category:</strong> {article.Category}</p>
    </div>
  );
};

export default Tile;