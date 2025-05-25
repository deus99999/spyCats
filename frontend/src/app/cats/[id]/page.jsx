'use client';

import { useRouter, useParams } from 'next/navigation'; // Правильно для App Router
import { useEffect, useState } from 'react';
import axios from 'axios';

const EditCatPage = () => {
  const router = useRouter();
  const params = useParams();
  const id = params.id; // Получаем 'id' из динамического маршрута [id]

  const [cat, setCat] = useState(null);
  const [salary, setSalary] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Улучшена проверка id: убедимся, что он существует и является числом
    // params.id всегда будет строкой, даже если в URL число.
    // Поэтому Number(id) и !isNaN(Number(id)) - хорошая практика.
    if (id && !isNaN(Number(id))) {
      setLoading(true);
      setError(null);
      axios.get(`http://127.0.0.1:8000/cat/${id}`)
        .then((res) => {
          setCat(res.data);
          setSalary(String(res.data.salary)); // Убеждаемся, что это строка для input
          setLoading(false);
        })
        .catch((err) => {
          console.error(err.response?.data || err.message || err);
          setError(err.response?.data?.detail);
          setLoading(false);
        });
    } else if (id === undefined) {         setLoading(false);
        setError('ID not in URL. Please navigate from the cat list.'); 
    } else { 
        setLoading(false);
        setError('Invalid cat ID in URL.'); 
    }
  }, [id]);

  const handleUpdate = async () => {
    setError(null);
    try {
      if (!id || isNaN(Number(id))) {
          setError('Invalid cat ID for update operation.'); 
          return;
      }
      await axios.patch(`http://127.0.0.1:8000/update-cat-salary/${id}`, {
        salary: Number(salary),
      });
      alert('Зарплата обновлена!');
      router.push('/');
    } catch (err) {
      console.error(err.response?.data || err.message || err);
      setError(err.response?.data?.detail );
    }
  };

  const handleDelete = async () => {
    setError(null);
    if (!window.confirm('Sure?')) {
        return;
    }
    try {
      
      await axios.delete(`http://127.0.0.1:8000/delete_cat/${id}`);
      router.push('/');
    } catch (err) {
      console.error( err.response?.data || err.message || err);
      setError(err.response?.data?.detail );
    }
  };

  if (loading) {
    return <div className=" text-center">Загрузка данных...</div>;
  }

  if (error) {
    return (
      <div className="py-3 rounded relative" role="alert">
        <strong className="font-bold">Ошибка!</strong>
        <span className="block sm:inline ml-2">{error}</span>
        <button onClick={() => router.back()} className="ml-4 underline">Назад</button>
      </div>
    );
  }

  if (!cat) { 
    return <div className="max-w-md mx-auto mt-10 p-6 text-center">Данные о кошке не найдены.</div>;
  }

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Edit: {cat.name}</h2>
      <label className="block mb-2">Salary:</label>
      <input
        type="number"
        value={salary}
        onChange={(e) => setSalary(e.target.value)}
        className="border border-gray-300 rounded px-3 py-2 w-full mb-4"
      />
      <div className="flex justify-between">
        <button
          onClick={handleUpdate}
          className="bg-orange-500 text-white px-4 py-2 rounded"
        >
          Update
        </button>
        <button
          onClick={handleDelete}
          className="bg-black text-white px-4 py-2 rounded"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default EditCatPage;