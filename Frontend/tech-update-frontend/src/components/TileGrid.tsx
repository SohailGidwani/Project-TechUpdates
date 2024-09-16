import React, { useState } from 'react';
import Tile from './Tile';
import { useFetchData } from '../hooks/useFetchdata.ts';
import { Article } from '../types/Article';

const TileGrid: React.FC = () => {
  const { data, loading, error } = useFetchData();
  const [upvotes, setUpvotes] = useState<{ [id: string]: number }>({});

  const handleUpvote = (title: string) => {
    setUpvotes((prev) => ({
      ...prev,
      [title]: (prev[title] || 0) + 1,
    }));
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="tile-grid">
      {data.map((article: Article) => (
        <Tile
          key={article.Title}
          article={{ ...article, Upvotes: upvotes[article.Title] || 0 }}
          onUpvote={handleUpvote}
        />
      ))}
    </div>
  );
};

export default TileGrid;
