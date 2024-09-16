import { useState, useEffect } from 'react';
import { Article } from '../types/Article';

const WEBHOOK_URL = 'https://webhook.site/d98d7020-811f-4d17-a838-5f4cb017054f';  // Replace with actual webhook

export const useFetchData = () => {
  const [data, setData] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(WEBHOOK_URL, { mode: 'no-cors' });
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const result = await response.json();
        setData(result);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};
