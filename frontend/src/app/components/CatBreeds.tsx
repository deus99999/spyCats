import React, { useEffect, useState } from 'react';
import Link from 'next/link';

const CatList = () => {
  const [cats, setCats] = useState([]);
  const [error, setError] = useState(null);

  const fetchCats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/cats');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCats(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchCats();
  }, []);

  

  if (error) {
    return (
      <div className="flex justify-center items-center h-48">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline ml-2">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="grid lg:grid-cols-5 gap-4 p-4">
        <div className="flex justify-end p-4">
            <Link href="/cats/create">
                <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                Create Cat
                </button>
            </Link>
            </div>
      {cats.map((cat) => (
        <div key={cat.id} className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col p-4">
          <h2 className="text-xl font-semibold mb-2">{cat.name}</h2>
          <p className="text-gray-600">Breed: {cat.breed}</p>
          <p className="text-gray-600">Experience: {cat.years_experience} years</p>
          <p className="text-gray-800 font-bold mb-2">Salary: ${cat.salary}</p>

          <div className="flex space-x-2">

            <Link href={`/cats/${cat.id}`}>
              <button className="bg-black text-white px-4 py-2 rounded mt-2">
                Edit
              </button>
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CatList;
